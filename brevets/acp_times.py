"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow

control_speedlimits = [(1000, 13.333, 26), (600, 11.428, 28), (400, 15, 30), (300, 15, 32), (200, 15, 32), (0, 15, 34)]

def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    
    #return false if greater than acceptable bounds
    if int(control_dist_km) > brevet_dist_km * 1.20:
        return False
    
    #set control dist to brev distance if within acceptable bounds of final control 
    if (int(control_dist_km) <= brevet_dist_km * 1.20 and int(control_dist_km) > brevet_dist_km):
        control_dist_km = brevet_dist_km
    
    #loop to calculate hour value and successively decrease control distance to change speed limits
    ohours = 0
    for dist, minspeed, maxspeed in control_speedlimits:
        if control_dist_km > dist:
            ohours += (control_dist_km - dist) / maxspeed
            control_dist_km = dist
    
    ###
    # need to get new arrowobject from start time to perform shift as the
    # argument requirements forced brevet_start_time to be in iso format
    ###
    opentime = arrow.get(brevet_start_time)
    return opentime.shift(hours=ohours).isoformat()


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    
    ###
    # return false if greater than acceptable bounds. only included for possible instructor
    # test cases as this error is handled solely by open_time func in flask_brevets.py file
    ###
    if int(control_dist_km) > brevet_dist_km * 1.20:
        return False
    
    #in case control distance is 0, meaning it's the first control, close in 1 hour
    closetime = arrow.get(brevet_start_time)
    if control_dist_km == 0:
        return closetime.shift(hours=1).isoformat()
    
    #set control to brevet dist if is within bounds of acceptable final distance
    if (int(control_dist_km) <= brevet_dist_km * 1.20 and int(control_dist_km) > brevet_dist_km):
        control_dist_km = brevet_dist_km
    
    #set to correct final endtime in case of special brevet dist
    if (int(control_dist_km) == brevet_dist_km): 
        if brevet_dist_km == 200:
            closetime = closetime.shift(minutes=10)
        if brevet_dist_km == 400:
            closetime = closetime.shift(minutes=20)
    
    #loop to change hours multiple and speed limits
    chours = 0 
    for dist, minspeed, maxspeed in control_speedlimits:
        if control_dist_km > dist:
            chours += (control_dist_km - dist) / minspeed
            control_dist_km = dist

    return closetime.shift(hours=chours).isoformat()

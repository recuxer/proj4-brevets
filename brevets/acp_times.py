"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow

#######################################
# Globals
##

#starting control hour shift
start_control_hour_shift = 1

#multiple to determine max allowed brevet control
max_brevet_distance_multiple = 1.20

#table of special endtimes for 200k and 400k brevets (brevdist, minute_shift_val)
brevet_max_times_shift = [(200, 10), (400, 20)]

#table of control speedlimits
control_speedlimits = [(1000, 13.333, 26), (600, 11.428, 28), (400, 15, 30), (300, 15, 32), (200, 15, 32), (0, 15, 34)]

#####################################
#function for determining opening times
def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    
    #return false if greater than acceptable bounds
    if int(control_dist_km) > brevet_dist_km * max_brevet_distance_multiple:
        return False
    
    #set control dist to brev distance if within acceptable bounds of final control 
    if (int(control_dist_km) <= brevet_dist_km * max_brevet_distance_multiple and int(control_dist_km) > brevet_dist_km):
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


#######################################
def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    
    #in case control distance is 0, meaning it's the first control, close in 1 hour
    closetime = arrow.get(brevet_start_time)
    if control_dist_km == 0:
        return closetime.shift(hours=start_control_hour_shift).isoformat()
    
    #set control to brevet dist if is within bounds of acceptable final distance
    if (int(control_dist_km) <= brevet_dist_km * max_brevet_distance_multiple and int(control_dist_km) > brevet_dist_km):
        control_dist_km = brevet_dist_km
    
    #set to correct final endtime in case of special brevet dist
    for brevdist, minshift in brevet_max_times_shift:
        if int(control_dist_km) == brevdist:
            closetime = closetime.shift(minutes=minshift)
 
    #loop to change hours multiple and speed limits
    chours = 0 
    for dist, minspeed, maxspeed in control_speedlimits:
        if control_dist_km > dist:
            chours += (control_dist_km - dist) / minspeed
            control_dist_km = dist

    return closetime.shift(hours=chours).isoformat()

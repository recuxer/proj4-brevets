"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow

#  Note for CIS 322 Fall 2016:
#  You MUST provide the following two functions
#  with these signatures, so that I can write
#  automated tests for grading.  You must keep
#  these signatures even if you don't use all the
#  same arguments.  Arguments are explained in the
#  javadoc comments.
#

#CONTROL_SPEEDS = [(0, 15, 34), (200, 34, 15), (400, 32, 15), (600, 30, 15), (1000, 28, 11.428), (1300, 26, 13.333)]
control_speedlimits = [(1000, 13.333, 26), (600, 11.428, 28), (400, 15, 30), (200, 15, 32), (0, 15, 34)]

def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
       brevet_dist_km: number, the nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    ohours = 0
    for dist, minspeed, maxspeed in control_speedlimits:
        if control_dist_km > dist:
            ohours += (control_dist_km - dist) / maxspeed
            control_dist_km = dist
    
    opentime = brevet_start_time
    
    #print(brevet_start_time.shift(hours=openhours).isoformat())
    #print(openhours)
    return opentime.shift(hours=ohours).isoformat()

def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
          brevet_dist_km: number, the nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    chours = 0 
    for dist, minspeed, maxspeed in control_speedlimits:
        if control_dist_km > dist:
            chours += (control_dist_km - dist) / minspeed
            control_dist_km = dist

    closetime = brevet_start_time
    print(chours)
    return closetime.shift(hours=chours).isoformat()
    #return arrow.now().isoformat()

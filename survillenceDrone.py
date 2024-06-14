'''
Drone Survillence - this makes drone move from series of points and make a circle after reaching each of the point then move to other checkpoint and so on. Uses very simple coding mechanism to perform this.
'''

from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import math
from pymavlink import mavutil


#alt - 598

waypoints = [
    # [lat, long, alt], 
    [30.27364549, 78.00030052, 10],
    [30.27382291, 77.99942743, 10],
    [30.27303044, 77.99943085, 10],
    [30.27256486, 78.00017202, 10]
]

## create a global vehicle that will be used in most functions
# only necessary if the file is run independently
vehicle = connect("127.0.0.1:14550",wait_ready=True)  
waypoint_counter = 1


# make circle in the same spot
def full_rotate():
    print("Doing a 360 !!")
    # Set desired heading (yaw angle)
    desired_heading = 360  # degrees (change this to your desired direction)

# Main loop
    try:
        # Send MAVLink command to control the vehicle's yaw
        msg = vehicle.message_factory.command_long_encode(
            0, 0,  # target system, target component
            mavutil.mavlink.MAV_CMD_CONDITION_YAW,  # command
            0,  # confirmation
            desired_heading,  # param 1 (yaw in degrees)
            20,  # param 2 (yaw rate: 20 deg/s)
            1,  # param 3 (0: absolute angle, 1: relative angle)
            1,  # param 4 (clockwise: 1, counterclockwise: -1)
            0,  # param 5 (empty)
            0,  # param 6 (empty)
            0   # param 7 (empty)
        )
        vehicle.send_mavlink(msg)
        
    # Wait for a short time to avoid flooding the system
        time.sleep(15)
        return True
    except KeyboardInterrupt as e:
        # Disarm the vehicle on keyboard interrupt
        print("Could not perform circle manuver !!")
        return False 
        
        

#move to waypoint
def start_mission(latitude, longitude, altitude):
    point = LocationGlobalRelative(latitude, longitude, altitude)
    vehicle.simple_goto(point)
    vehicle.airspeed = 10
    # Wait for the drone to reach the target
    tolerance = 0.00001
    while True:
        current_latitude = vehicle.location.global_relative_frame.lat
        current_longitude = vehicle.location.global_relative_frame.lon
        current_altitude = vehicle.location.global_relative_frame.alt
        print(f"lat: {current_latitude} :: long : {current_longitude} :: alt : {current_altitude}")
        distance_latitude = abs(latitude-current_latitude)
        distance_longitude = abs(longitude-current_longitude)
        if distance_latitude <= tolerance and distance_longitude <= tolerance:
            print(f"Reached Waypoint {waypoint_counter}!!")
            # Check for library functions to get current location or implement a callback
            #  to perform actions after reaching the waypoint
            return full_rotate()
        time.sleep(2)


# arm and launch the drone
def initiate_drone():
    target_altitude = 10
    # connect
    
    # arm the drone 
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Armed Successfully !")
    time.sleep(2)
    print("Taking off!")
    vehicle.simple_takeoff(target_altitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto
    #  (otherwise the command after Vehicle.simple_takeoff will execute
    #   immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= target_altitude * 0.95:
            print("Reached target altitude")
            break
    time.sleep(1)


initiate_drone()  #only necessary if the file is used standalone
# move the drone to different checkpoints
print("Starting Surveying....")
time.sleep(2)
# traversing all the waypoints to move the drone to each one of them
for coordinates in waypoints:
    latitude, longitude, altitude = coordinates
    print(f"moving to {waypoint_counter} waypoint")
    mission_status = start_mission(latitude, longitude, altitude)
    if not mission_status: # if got false due to any reason
        print("could not reach waypoint..Terminating the script")
        vehicle.mode = VehicleMode("RTL")
        vehicle.close()
    waypoint_counter+=1
# return the drone to home location once the job is complete 
print("Survillence completed, returning to base!!")
vehicle.mode = VehicleMode("RTL")

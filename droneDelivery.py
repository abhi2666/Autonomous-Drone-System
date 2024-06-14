from __future__ import print_function
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative
from math import *

## manually inserting the connection port
# Set up option parsing to get connection string
# import argparse
# parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
# parser.add_argument('--connect',
#                     help="Vehicle connection target string. If not specified, SITL automatically started and used.")
# args = parser.parse_args()

# connection_string = args.connect
# sitl = None


# # Start SITL if no connection string specified
# if not connection_string:
#     import dronekit_sitl
#     sitl = dronekit_sitl.start_default()
#     connection_string = sitl.connection_string()
home_lat, home_long = 30.272883468400977, 78.0003869533539
### destination - -35.36214714 149.16507026

# Connect to the Vehicle
vehicle = connect("127.0.0.1:14550",wait_ready=True)
print("Connected to the port 127.0.0.1:14550 successfully !")

def arm_and_takeoff(target_altitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
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

#### check for validity of latitude and longitude ####
def isValid(latitude, longitude):
    if latitude < -90 or latitude > 90:
        return False

  # Valid longitude ranges from -180 to 180 degrees
    if longitude < -180 or longitude > 180:
        return False

    return True

#### countdown ####
def countdown(seconds):
  """
  This function counts down from the given number of seconds 
  and prints the remaining time.
  """
  while seconds > 0:
    # minutes = int(seconds / 60)
    remaining_seconds = seconds % 60
    print("Will Fly to Base in ", remaining_seconds, " seconds")
    # Wait for 1 second before updating the timer
    time.sleep(1)
    seconds -= 1


#### land the drone and hold for few seconds for parcel recovery ######
def land_and_hold():
    print("Landing...")
    print("Vehicle in LAND mode")
    vehicle.mode = VehicleMode("LAND")

    try:
        vehicle.airspeed = 1
    except Exception as e:
        print("can't increaes the speed..")

    while True:
        #check = True
        ## adjust the speed at the last second
        # if check and vehicle.location.global_frame.alt < 10:
        #     check = False
        #     vehicle.airspeed = 1

        if vehicle.location.global_relative_frame.alt<=1:
            print("Vehicle Landed Successfully !")
            print("Pick up the parcel yourself !!")
            # countdown(10) ## countdown for 10 seconds
            break
        else:
            print("Altitiude : ", vehicle.location.global_relative_frame.alt)
            time.sleep(2)
        # if vehicle.location.global_relative_frame.alt < 2:
        #     set_velocity_body(vehicle,0,0,0.1)
    # print ("Vehicle in AUTO mode")
    # vehicle.mode = VehicleMode("AUTO")
    


def move_to_waypoint(destination_latitude, destination_longitude):
    max_wait_time = 30 ## after 30 seconds the drone will return to the base if canno reach the target location
    start_time = time.time()
    print("Moving towards wpl..")
    point1 = LocationGlobalRelative(destination_latitude, destination_longitude, 50)
    vehicle.simple_goto(point1)

    # Wait for the drone to reach the target
    tolerance = 0.00001
    while True:
        latitude = vehicle.location.global_relative_frame.lat
        longitude = vehicle.location.global_relative_frame.lon
        distance_latitude = abs(destination_latitude-latitude)
        distance_longitude = abs(destination_longitude-longitude)
        if distance_latitude <= tolerance and distance_longitude <= tolerance:
            print("Reached Waypoint")
            # Check for library functions to get current location or implement a callback
            #  to perform actions after reaching the waypoint
            return True
        if time.time() - start_time >= max_wait_time:
            print("Timeout: Drone did not reach waypoint within", max_wait_time, "seconds")
            return False

        print("Waiting for drone to reach waypoint...")
        time.sleep(2) 


'''
temp target location -> 30.27381473 77.99944552 
'''

############## MAIN ##################

def initiate_drone():
    print("Welcome to Drone Delivery System")
    target_altitude = int(input("Enter target Altitude: "))
    destination_latitude, destination_longitude = 0.0, 0.0

    while True:
        lat, long = map(float, input("Enter latitude and longitude of the destination: ").split())
        if isValid(lat, long):
            destination_latitude, destination_longitude = lat, long
            break
        else:
            print("Please enter valid coordinates\n")


    ######## Arming the Drone and Taking Off ###########
    try:
        arm_and_takeoff(target_altitude)
    except Exception as e:
        print(f"Something went wrong {e}")

    print("Setting airspeed to 10...")
    vehicle.airspeed = 10

    ## move to waypoint -- eventually will be true
    hasReached = move_to_waypoint(destination_latitude, destination_longitude)
    time.sleep(2)
    missionCompleted = False
    if hasReached:
        ## land at the destination
        land_and_hold()
        # arm_and_takeoff(target_altitude)
        vehicle.mode = VehicleMode("GUIDED")
        # vehicle.armed = True
        print("Delivered the parcel successfully")
        time.sleep(5)
        print("Returning to Base...")
        vehicle.mode = VehicleMode("RTL")
        missionCompleted = True
    else:
        print("Could not reach the waypoint !")
        print("Returning to base...")
        vehicle.mode = VehicleMode("RTL")

    # Close vehicle object before exiting script
    print("Terminating Connection with SITL Drone...")
    vehicle.close()
    print("Closing..")
    return missionCompleted

initiate_drone() # for using the file as standalone script
from dronekit import connect, VehicleMode
import time
from pymavlink import mavutil

def temp_connection():
    # Connect to the ArduPilot SITL instance
    vehicle = connect('udp:127.0.0.1:14550', wait_ready=True)

    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Armed Successfully !")
    time.sleep(2)
    print("Taking off!")
    target_altitude = 10
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
    

## main function 
def full_rotate(vehicle):
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
        time.sleep(0.1)
    except KeyboardInterrupt as e:
        # Disarm the vehicle on keyboard interrupt
        vehicle.armed = False
        print("Vehicle disarmed.")

# Close connection
# vehicle.close()


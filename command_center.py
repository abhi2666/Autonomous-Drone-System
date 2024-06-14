import droneDelivery, survillenceDrone
## initiate the drone
vehicle = connect("127.0.0.1:14550",wait_ready=True)
print("Connected to the port 127.0.0.1:14550 successfully !")
print("Autonomous Drone System")
print("1. Start Drone Delivery system")
print("2. Start Survillence system")
print("3. Exit the program")
while True:
    
    choice = int(input("Enter choice : "))

    if choice == 1:
        print("starting drone delivery system")
        drone_status = droneDelivery.initiate_drone()
    elif choice ==2:
        print("starting survillence system")
        survillenceDrone.droneSurvey()
    elif choice == 'q':
        print("Exiting the program..")
        break
    else:
        print("Enter valid choice")




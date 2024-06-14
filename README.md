# Autonomous-Drone-System
Automated drone system Ardupilot and Dronekit capable of performing various feats.
-> The Project features an autopilot / simulator that uses Ardupilot at its core. But if you have the right set of components, then you can try it directly on your drone.
-> Simulator provides a safe way of testing the drone and the tension of breaking expensive parts will be no more.

NOTE -> If you are want to try this code for yourself, then please contact at gairolaabhishek26@gmail.com because the setup is not easy !

Features - 
1. Drone Delivery - capable of performing drone delivery where it starts from your home location and then go to your desired location. You have the freedom of choosing the altitude and target location and based of that the drone will take the shortest path. 

NOTE - Since its a simulation, the drone does not perform any object detection and object avoidance, but if you have an actual camera drone then you can add the required extra lines of code to make object detection and avoidance drone. You will need some extra sensors like lidar.

2. surveillance - perform surveillance of marked area and hovering over certain fixed points (geo location) and then performing designated manuvers. Can cover larger or smaller area.
Can be enhanced easily by using a good camera and multiple drones at the same time.

NOTE - you need GPS enabled drone to perfrom both the tasks because that is how the drone will keep track of its location with respect to target location.

![Screenshot (261)](https://github.com/abhi2666/Autonomous-Drone-System/assets/95623413/137ac4d9-baef-4656-916f-60cf6b7a553e)
![Screenshot (246)](https://github.com/abhi2666/Autonomous-Drone-System/assets/95623413/691a6bba-079e-46f7-8a39-a244ccbc1cc0)


Softwares and Libraries Required -

1. Ubuntu 20.04
2. Ardupilot - you will need to install this inorder to use the autopilot. You can see the 2D view of your simulated drone in map (map is part of ardupilot and opens automatically with the ardupilot software).
3. Dronekit - this library is used for actually programming the drone to perfrom the task. Can be used to program both simulated and physical drone.
4. Mavlink & Mavproxy - mavlink is the communication protocol that we will use communicate with the drone through GCS (Ground Control Station) and mavproxy is the command line itself where we will use the mavlink.
5. Gazebo - this software is essential if you want to see the 3D overview of your simnulated drone. It connectes with GCS through mavproxy and then can use the GCS data to show 3D simulation of the drone.
NOTE - to use Gazebo, you will need a good amount of graphical memory and therefore using a VM may not be the best option. Though you can use VM but the 3D visualization will be choppy and laggy.

Python Version used - 3.8 and 3.9.14 are the two versions that were used. You can have only 3.9.14 as well and it will still work.

How to install - 

Follow the step by step guide in the ardupilot webiste to install it and then install dronekit seperately. You may need to install some other libraries as well in order to install all these. For gazebo, install the noetic version, which was used in this project.

GAZEBO 3D view -


![Screenshot (290)](https://github.com/abhi2666/Autonomous-Drone-System/assets/95623413/5c4ac918-f4ea-4e49-9ee8-b7528191e648)

For brief overview please contact using the above mail.

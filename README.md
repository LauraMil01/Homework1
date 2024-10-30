# Homework1
READ ME
-To visualize the robot in rviz2 use the following command:
$ros2 launch arm_description display.launch.py
When rviz2 is open, to visualize the robot it’s necessary set the voice “Fixed frame” = “world”, add “RobotModel” and set in it the voice “Description Topic” = “/robot_description”

-To spawn the robot in Gazebo with the use of controllers use the following command:
$ros2 launch arm_gazebo arm_gazebo.launch.py

-After spawning the robot in Gazebo, to view the images given by the camera use the following command:
$ros2 run rqt_image_view rqt_image_view
When rqt_image_view is open, to view the image it’s necessary select “/videocamera”

-After spawning the robot in Gazebo, to run the node talk_list:
$ros2 run arm_controller talk_list
In another terminal, to publish the joints’ position via command line we use:
$ros2 topic pub JointPositionController/commands std_msgs/msg/Float64MultiArray "{data: [0 ,0, 0, 0]}"
(you can change the values in data)

-We have added a record of the robot changing its configuration. To rewatch the record, we write on terminal this command:
$ros2 launch arm_gazebo arm_gazebo.launch.py
and on another terminal, we write:
$cd src/bag_files/rosbag2_2024_10_29-20_18_22
$ros2 bag play rosbag2_2024_10_29-20_18_22_0.db3

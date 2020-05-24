ls
rostopic list
rviz
cd catkin_ws/src/
catkin_create_pkg summit_description rospy rviz controller_manager gazebo_ros joint_state_publisher robot_state_publisher
roslaunch summit_description summit.launch 
rosrun xacro xacro /home/user/src/summit_description/robot/summit.urdf.xacro
pwd
rosrun xacro xacro /home/user/src/summit_description/robot/summit.urdf.xacro
rosrun xacro xacro /home/user/catkin_ws/src/summit_description/robot/summit.urdf.xacro
clear
rosrun xacro xacro /home/user/catkin_ws/src/summit_description/robot/summit.urdf.xacro
roslaunch summit_description/ summit.launch
roslaunch summit_description summit.launch 
cp summit_description/ /usr/share/gazebo/models/
cp -r summit_description/ /usr/share/gazebo/models/
roslaunch summit_description summit.launch 

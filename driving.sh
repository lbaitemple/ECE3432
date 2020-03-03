export ROS_IP=`hostname  -I |sed 's/ //g'`
export ROS_MASTER_URI=http://$ROS_IP:11311
cd catkin_ws
catkin_make
source devel/setup.bash
roslaunch simp_motor start.launch

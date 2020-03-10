export MASTERIP=10.110.41.228
export ROS_MASTER_URI=http://$MASTERIP:11311
export ROS_IP=`hostname  -I |sed 's/ //g'`

cd teleop_ws
catkin_make
source devel/setup.bash
rosrun subimage readData.py

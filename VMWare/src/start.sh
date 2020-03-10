##you can use img or csv format to save file
export FORMAT="img"
## add raspberry pi IP address, please start script in raspberry pi first
export MASTERIP=10.110.42.68
export ROS_MASTER_URI=http://$MASTERIP:11311
export ROS_IP=`hostname  -I |sed 's/ //g'`


cd teleop_ws
catkin_make
source devel/setup.bash
rosrun subimage readData.py

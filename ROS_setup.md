After you install the ROS system, you can setup a workspace. 

```

sudo apt install ros-melodic-joy -y
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws
catkin_make
cd ~/catkin_ws/src
fetcher --url="https://github.com/lbaitemple/ECE3432/tree/master/simp_motor"
chmod +x simp_motor/src/Joydrive22Revision1.py
cd ~/catkin_ws
rosdep install --from-paths src --ignore-src -r -y
catkin_make
cd ~
fetcher --url="https://github.com/lbaitemple/ECE3432/blob/master/driving.sh"
chmod +x driving.sh
./driving.sh
```

After you install the ROS system, you can setup a workspace. 

```

sudo apt install ros-melodic-joy -y
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws
catkin_make
cd ~/catkin_ws/src
fetcher --url="https://github.com/lbaitemple/ECE3432/tree/master/simp_motor"
chmod +x simp_motor/src/Joydrive22Revision1.py
pip install Adafruit_PCA9685
cd ~/catkin_ws
rosdep install --from-paths src --ignore-src -r -y
catkin_make
cd ~
fetcher --url="https://github.com/lbaitemple/ECE3432/blob/master/driving.sh"
chmod +x driving.sh
./driving.sh
```


Setup Camera System

```
sudo add-apt-repository ppa:ubuntu-raspi2/ppa
sudo apt-get update
sudo apt-get install linux-raspi2 libraspberrypi-bin  libraspberrypi-bin-nonfree -y
sudo chmod 777 /dev/vchiq
sudo apt-get install libjpeg8-dev imagemagick libv4l-dev -y
sudo apt-get install libopencv-core-dev libopencv-dev libraspberrypi-dev -y
sudo dpkg -i --force-overwrite   /var/cache/apt/archives/libraspberrypi-dev_1.20161003.2350bf2-1_armhf.deb
sudo apt-get install python3-pip -y
sudo usermod -a -G video $USER
sudo pip3 install picamera
```
### enable raspi-cam
add content in config.txt
```
start_x=1             # essential
gpu_mem=128           # at least, or maybe more if you wish
disable_camera_led=1  # optional, if you don't want the led to glow
```

review
```
raspivid -t 0
```
runt the python file
```
wget https://raw.githubusercontent.com/lbaitemple/ubuntu_server_rpi/master/torch/rpi_camera_surveillance_system.py
python3 rpi_camera_surveillance_system.py
```

Then you can check the video stream by using a browser window by typing http://[pi_ip]:8000

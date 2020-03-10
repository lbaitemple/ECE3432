In VM Guest OS, you will need to do the following commands

#### step 1: utility to download a subfolder or a file in a Github link

```
sudo apt-get install nodejs-dev node-gyp libssl1.0-dev -y
sudo apt-get install npm -y
sudo npm install -g github-files-fetcher
fetcher --url="hyper_link"
```
#### step 2: Create a ROS workspace and install the rospackage
```
mkdir -p ~/teleop_ws/src
cd ~/teleop_ws
catkin_make
cd ~/teleop_ws/src
fetcher --url="https://github.com/lbaitemple/ECE3432/tree/master/VMWare/src/subimage"
chmod +x subimage/src/readData.py
cd ~/teleop_ws
fetcher --url="https://github.com/lbaitemple/ECE3432/blob/master/VMWare/src/settings.json"
rosdep install --from-paths src --ignore-src -r -y
catkin_make
cd ~
fetcher --url="https://github.com/lbaitemple/ECE3432/blob/master/VMWare/src/start.sh"
chmod +x start.sh
```
Please review the first line to modify your raspberry pi IP address in the script, then you can run
```
./start.sh
```
When you need to stop, press Ctrl-C to quit.


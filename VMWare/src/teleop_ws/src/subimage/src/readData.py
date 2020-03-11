#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
from PIL import Image
import requests
from StringIO import StringIO
from SuironIO import SuironIO
from clock import Clock
import json, urllib, cv2
import numpy as np
import os
from threading import Lock


DATAFORMAT=os.environ['FORMAT']

with open('./settings.json') as d:
    SETTINGS = json.load(d)

suironio = SuironIO(id=0, width=SETTINGS['width'], height=SETTINGS['height'], depth=SETTINGS['depth'])
suironio.init_saving()
lock = Lock()
clck=Clock(suironio, 0.01)
clck.start()


def getimage(link):
    print("get image " + link)
    stream = urllib.urlopen(link)
    bytes = ''
    i=''
    while True:
        bytes += stream.read(1024)
        a = bytes.find('\xff\xd8')
        b = bytes.find('\xff\xd9')
        if a != -1 and b != -1:
            jpg = bytes[a:b+2]
            bytes = bytes[b+2:]
            i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), 1)
            break; 
    return i

def callback(data):
    print("call back")
    lock.acquire()
    if (not suironio.check_lock()):

#        rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.axes[2])
#        response = requests.get('http://10.108.30.205:8000/stream.mjpg')
        print(os.environ['MASTERIP'])
        ret =getimage('http://'+os.environ['MASTERIP']+':8000/stream.mjpg')
#        print(ret)
        img = ret
#        response.close()

        turn=abs(0.05*data.axes[2]-0.15)
        speed = abs(-0.05*data.axes[1]-0.15)
        print(turn, speed)
        s={}
        s['motor']=speed
        s['servo']=turn
        print("Recording Inputs...")
        suironio.record_inputs(s, np.array(img), DATAFORMAT)
        suironio.unlock()

    lock.release()
    print("releasing")


def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)
    sub=rospy.Subscriber("joy", Joy, callback, queue_size=1, tcp_nodelay=True, buff_size=2**24)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    while  not rospy.is_shutdown():
        try:
            listener() 
        except KeyboardInterrupt:
            break

    print('Saving file...')
    clck.stop()

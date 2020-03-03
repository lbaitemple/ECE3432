#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32
from sensor_msgs.msg import Joy
from std_msgs.msg import String
import settings
from settings import wiringport
import os,sys, select, termios, tty
import json
import time
#from datetime import datetime
# Import the PCA9685 module.
#This is for REV 2.2
# import Adafruit_PCA9685

# Initialise the PCA9685 using the default address (0x40).
#pwm = Adafruit_PCA9685.PCA9685(0x40)

# pwm.set_pwm_freq(92.7)
#now = datetime.now()
#nowtime = now.strftime("%H:%M:%S:%f")
maxspeed = 0.17
minspeed = 0.13
nos = os.system
s0 = wiringport[settings.PINS['servo0']]
s1 = wiringport[settings.PINS['servo1']]
cmd= ["gpio mode {} pwm".format(s0),
     "gpio mode {} pwm".format(s1),
     "gpio pwm-ms",
     "gpio pwmc 1920",
     "gpio pwmr 100",
 ]


def setspeed(pin, sped):
    if (pin==12):
        str="gpio pwm {} {}".format(s0, sped*100)
        nos(str)
    elif (pin==13):
        str="gpio pwm {} {}".format(s1, sped*100)
        nos(str)


#def on_new_servo(data):
#    pwm.set_pwm(9, 0, int(data.data))
#    setspeed(13, data.data)
def callback(data):
#    rate = rospy.Rate(20)
#    print(data.axes[0], data.axes[1], data.axes[2])
#    twist.angular.x = abs(0.05*data.axes[0]-0.15)
    turn = abs(0.05*data.axes[0]-0.15)
#    twist.linear.x = 0.05*data.axes[1]+0.15
    speed  = 0.05*data.axes[1]+0.15    
#    print(twist)
#    pwm.set_pwm(8, 0, int(speed))
    if speed > maxspeed:
        speed = maxspeed
    elif speed < minspeed:
        speed = minspeed
    print("This is Motor values" , speed)
    setspeed(12, speed)
    print("This is servo values" , turn)
    setspeed(13, turn) 
#    pub.publish(twist)
#    rate.sleep()

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('motor_car', anonymous=True)
   # subscriber_twist = rospy.Subscriber("cmd_vel", Twist, on_new_twist, queue_size=10)
    rospy.Subscriber("joy", Joy, callback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    for i in range(0, len(cmd)):
        nos(cmd[i])
        print(cmd[i])
#    print(nowtime)
    listener()


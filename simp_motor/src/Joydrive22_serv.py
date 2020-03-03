#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from simple_motor.srv  import *
from std_msgs.msg import Float32
from std_msgs.msg import String
import settings
from settings import wiringport
import os,sys, select, termios, tty
import json
import time

# Import the PCA9685 module.
#This is for REV 2.2
# import Adafruit_PCA9685

# Initialise the PCA9685 using the default address (0x40).
#pwm = Adafruit_PCA9685.PCA9685(0x40)

# pwm.set_pwm_freq(92.7)
NAME = 'drive_server'
s0 = wiringport[settings.PINS['servo0']]
s1 = wiringport[settings.PINS['servo1']]

cmd= ["gpio mode {} pwm".format(s0),
     "gpio mode {} pwm".format(s1),
     "gpio pwm-ms",
     "gpio pwmc 1920",
     "gpio pwmr 100",
 ]

def drive(req):
#    print(req.speed, req.turn)
    setspeed(12, int(req.speed))
    setspeed(13, int(req.turn))
#    print(req.speed, req.turn)
#    print("Returning [%s + %s ]" %(req.speed, req.turn))
    return DriveResponse(req.speed + req.turn)

def setspeed(pin, sped):
    if (pin==12): # speed
        str="gpio pwm {} {}".format(s0, sped)
#        print(str)
        os.system(str)
    elif (pin==13): # turn
        str="gpio pwm {} {}".format(s1, sped)
        os.system(str)

#def on_new_twist(data):
#    pwm.set_pwm(8, 0, int(data.linear.x))
#    print("This is Motor values" , data.linear.x)
#    setspeed(12, data.linear.x)
#    print("This is servo values" , data.angular.x)
#    setspeed(13, data.angular.x)

#def on_new_servo(data):
#    pwm.set_pwm(9, 0, int(data.data))
#    setspeed(13, data.data)

def drive_server():

    rospy.init_node(NAME)
    #subscriber_twist = rospy.Subscriber("cmd_vel", Twist, on_new_twist, queue_size=10)
    s = rospy.Service('drive', Drive, drive)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    for i in range(0, len(cmd)):
#        print(cmd[i])
        os.system(cmd[i])

    drive_server()


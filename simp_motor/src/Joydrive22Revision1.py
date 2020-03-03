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
import Adafruit_PCA9685

#-----------------------------------------------------------------
REV = 2.3 # select your board 
# If your board has a PWM module built in we will need the correct chip
if REV == 2.3:
#    import Adafruit_PCA9685
# Initialise the PCA9685 using the default address (0x40).
    pwm = Adafruit_PCA9685.PCA9685(0x40)
#    pwm.set_pwm_freq(97.1)
    pwm.set_pwm_freq(93.7)
#-------------------------------------------------------------
#---------------------------------------------------------------
#These are used to adjust driving
x = 0.0175
x_button = 1


#-------------------------------------------------------------

#Our attempt to speed up the process
nos = os.system

if REV == 2.2:
    s0 = wiringport[settings.PINS['servo0']]
    s1 = wiringport[settings.PINS['servo1']]
    cmd= ["gpio mode {} pwm".format(s0),
         "gpio mode {} pwm".format(s1),
         "gpio pwm-ms",
         "gpio pwmc 1920",
         "gpio pwmr 100", ]


def setspeed22(pin, sped):
    if (pin==12):
        str="gpio pwm {} {}".format(s0, sped*100)
        nos(str)
    elif (pin==13):
        str="gpio pwm {} {}".format(s1, sped*100)
        nos(str)

def setspeed23(pin, sped):
    pos = int(sped*4096)
    print(pos)
    pwm.set_pwm(pin, 0, pos)

def callback(data):
    global x 
    global x_button 
    turn = abs(0.05*data.axes[2]-0.15)
    speed = abs(-0.05*data.axes[1]-0.15)
#    speed  = x_button *x*data.buttons[6]+0.15
    pwm.set_pwm(8, 0, int(speed))

    if REV == 2.2:
        print("This is Motor values" , speed)
        setspeed22(12, speed)
        print("This is servo values" , turn)
        setspeed22(13, turn)
    elif REV == 2.3:
        print("This is Motor values for 2.3" , speed)
        setspeed23(8, speed)
        print("This is Motor values for 2.3" , turn)
        setspeed23(9,turn)
 #   if data.buttons[5] == 1:
 #       x_button = -1 * x_button
 #       print("reverse mode")
 #   if data.axes[5] == 1:
 #       x = x + 0.005
 #   if data.axes[5] == -1:
 #       x = x - 0.005
#    pub.publish(twist)
#    rate.sleep()

def listener():
    rospy.init_node('motor_car', anonymous=True)
    rospy.Subscriber("joy", Joy, callback)
    rospy.spin()    # spin() simply keeps python from exiting until this node is stopped


#START

REV == 2.3
if __name__ == '__main__':
    if REV == 2.2:
        for i in range(0, len(cmd)):
            nos(cmd[i])
            print(cmd[i])
    listener()

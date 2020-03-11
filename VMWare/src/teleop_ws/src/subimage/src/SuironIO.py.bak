import time
import random
import numpy as np
import pandas as pd
import cv2, os, csv
import matplotlib.pyplot as plt
from functions import cnn_to_raw
from img_serializer import serialize_image
from file_finder import get_new_filename
import clock 

class SuironIO(clock.Action):
    """
    Class which handles input output aspect of the suiron 
    - Reads inputs from webcam and normalizes them
    - Also reads serial input and write them to file
    """

    # Constructor
    def __init__(self, id=1, width=72, height=48, depth=3, baudrate=57600):
        # Image settings
        self.width = int(width)
        self.height = int(height)
        self.depth = int(depth)
        self.sz=self.width *self.height  *self.depth 
        self.locked = False 
        # Video IO 
#        self.cap =  cv2.VideoCapture(id) # Use first capture device

        # Serial IO
        self.outfile = None        
        self.header= False
        # In-memory variable to record data
        # to prevent too much I/O
        self.frame_results = []
        self.servo_results = []
        self.motorspeed_results = [] 
    
    """ Functions below are used for inputs (recording data) """
    # Initialize settings before saving 
    def init_saving(self, folder='data', filename='output_', extension='.csv'):
        fileoutname = get_new_filename(folder=folder, filename=filename, extension=extension)

        # Filename to save serial data and image data
        # Output file
        print(fileoutname)
        outfile = open(fileoutname, 'w') # Truncate file first
        self.outfile = open(fileoutname, 'a')
        self.df = pd.DataFrame([], columns=['image', 'servo', 'motor'])
        self.df.to_csv(self.outfile)
        self.header = True


    def start(self, period):
        thread=clock.Clock(self, period)
        thread.start()
        return thread

    def run(self):
        time.sleep(0.01)
    # Saves both inputs
    def lock(self, locked = True):
        self.locked = locked
    def unlock(self):
        self.locked = False
    def check_lock(self):
        return self.locked
    def record_inputs(self, s_inputs, frame):
        # Frame is just a numpy array
        if (not self.check_lock()):
#            frame = self.get_frame()
            self.lock()
        # Serial inputs is a dict with key 'servo', and 'motor'

        # If its not in manual mode then proceed
#        print("yeah")
#        print("helllo {}".format(s_inputs))
            if s_inputs:
                servo = s_inputs['servo'] 
                motor = s_inputs['motor'] 

            # Append to memory
            # tolist so it actually appends the entire thing
                frame=self.normalize_frame(frame)
                dat=serialize_image(frame)
                print(frame.shape, len(dat))
#                if (len(dat)==self.sz):
                self.frame_results.append(dat)
#            print(serialize_image(frame))
                self.servo_results.append(servo)
                self.motorspeed_results.append(motor)
    		self.append_inputs()
                self.unlock()
    # Gets frame
    def get_frame(self):
        ret, frame = self.cap.read()
    
        # If we get a frame, save it
        if not ret:
            raise IOError('No image found!')

        frame = self.normalize_frame(frame)
        
        return frame

    # Gets frame
    def get_camframe(self):
        ret, frame = self.cap.read()
        return(frame)

    # Gets frame for prediction
    def get_frame_prediction(self):
        ret, frame = self.cap.read()

        # if we get a frame
        if not ret:
            raise IOError('No image found!')

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (self.width, self.height), interpolation=cv2.INTER_CUBIC)
        frame = frame.astype('uint8')

        return frame
    

    # Normalizes inputs so we don't have to worry about weird
    # characters e.g. \r\n
    def normalize_serial(self, line):
        # Assuming that it receives 
        # servo, motor
        
        # 'error' basically means that 
        # its in manual mode
        try:
            line = line.replace('\n', '').split(',')
            line_dict = {'servo': int(line[0]), 'motor': int(line[1])}
            return line_dict
        except:
            return None

    # Normalizes frame so we don't have BGR as opposed to RGB
    def normalize_frame(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (self.width, self.height), interpolation=cv2.INTER_CUBIC)
        frame = frame.flatten()
        frame = frame.astype('uint8')
        return frame

    # Saves files
    def save_inputs(self):
        raw_data = {
            'image': self.frame_results, 
            'servo': self.servo_results,
            'motor': self.motorspeed_results
        }
        df = pd.DataFrame(raw_data, columns=['image', 'servo', 'motor'])
        df.to_csv(self.outfile)

    # Saves files
    def append_inputs(self):
        raw_data = {
            'image': self.frame_results, 
            'servo': self.servo_results,
            'motor': self.motorspeed_results
        }
#        df = pd.DataFrame(raw_data, columns=['image', 'servo', 'motor'])
#        df.to_csv(self.outfile)
        if (self.header):
            self.df = pd.DataFrame(raw_data, columns=['image', 'servo', 'motor'])
            self.df.to_csv(self.outfile, mode='a', header=False)
            self.frame_results = []
            self.servo_results = []
            self.motorspeed_results = [] 

        else:
            self.df = pd.DataFrame(raw_data, columns=['image', 'servo', 'motor'])
            self.df.to_csv(self.outfile)
            self.header=True


    """ Functions below are used for ouputs (controlling servo/motor) """    
    # Controls the servo given the numpy array outputted by
    # the neural network
    def servo_write(self, np_y):
        servo_out = cnn_to_raw(np_y)

        if (servo_out < 90):
            servo_out *= 0.85

        elif (servo_out > 90):
            servo_out *= 1.15

        self.ser.write('steer,' + str(servo_out) + '\n') 
        time.sleep(0.02)

    # Sets the motor at a fixed speed
    def motor_write_fixed(self):    
        self.ser.write('motor,80\n')
        time.sleep(0.02)

    # Stops motors
    def motor_stop(self):      
        self.ser.write('motor,90\n')
        time.sleep(0.02)

    # Staightens servos
    def servo_straighten(self):
        self.ser.write('steer,90')
        time.sleep(0.02)
        
    def __del__(self):
        if self.outfile:
            self.outfile.close()

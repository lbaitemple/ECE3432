import json
import pandas as pd
import numpy as np
import cv2
from model import Model1
from model import Model2

class CarDataFile:
    def __init__(self, dfile='output_0.csv', dwidth=640, dheight=320):
        self.data = pd.read_csv(dfile)
        self.len = len(self.data)
        self.width=dwidth
        self.height= dheight
        self.servo_model = Model1()
        self.motor_model = Model2()
        self.badindx=[]
        with open('settings.json') as d:
            SETTINGS = json.load(d)

        self.servo_model.loadmodel(SETTINGS['servo_cnn_name'] + '.pth')
        self.motor_model.loadmodel(SETTINGS['motor_nn_name'] + ".pth")

    def getImage(self, indx=0):
        cur_img = self.data['image'][indx]
        cur_img = np.fromstring(cur_img[1:-1], sep=', ', dtype='uint8')
        with open('settings.json') as d:
            SETTINGS = json.load(d)

        width = SETTINGS['width']
        height = SETTINGS['height']
        depth = SETTINGS['depth']
        cur_img = np.resize(cur_img, (height, width, depth))


        return cur_img

    def display(self, indx=0, cmd=ord(' '), nfile='data.csv'):
        if (cmd==ord('d')):
            self.badindx.append(indx-1)
        elif (cmd==ord('s')):
            sadata =  self.data[0:indx]
            sadata=self.data.drop(sadata)
            sadata.to_csv(nfile)
        cur_throttle = int(self.data['servo'][indx] * 100)
        cur_img = self.getImage(indx)


        cur_img_array = cv2.resize(cur_img, (self.width, self.height), interpolation=cv2.INTER_CUBIC)
        cv2.line(cur_img_array, (240, 300), (240 - 20*(15 - cur_throttle), 200), (255, 0, 0), 3)
        cv2.imshow('picture {}'.format(indx), cv2.cvtColor(cur_img_array, cv2.COLOR_RGB2BGR))
        cur_img_array = cv2.putText(cur_img_array, str(cur_throttle), (180, 310),  cv2.FONT_HERSHEY_SIMPLEX,
                            1, (255,255,255), 2, cv2.LINE_AA)

    def display_pred(self, indx=0):
        cur_throttle = int(self.data['servo'][indx] * 100)
        cur_motor = int(self.data['motor'][indx] * 100)
        cur_img = self.getImage(indx)
        pred_throttle, pred_motor =  self.predict(indx)
        pred_throttle=int(pred_throttle*100)

        # print(self.width, self.height)
        cur_img_array = cv2.resize(cur_img, (self.width, self.height), interpolation=cv2.INTER_CUBIC)
        cv2.line(cur_img_array, (240, 280), (240 - 20*(15 - cur_throttle), 100), (255, 0, 0), 3)
        cv2.line(cur_img_array, (220, 280), (220 - 20*(15 - pred_throttle), 100), (255, 255, 0), 3)
        cur_img_array = cv2.putText(cur_img_array, str(cur_throttle) + ":" + str(pred_throttle), (180, 310),  cv2.FONT_HERSHEY_SIMPLEX,
                            1, (255,255,255), 2, cv2.LINE_AA)

        cv2.imshow('picture {}'.format(indx), cv2.cvtColor(cur_img_array, cv2.COLOR_RGB2BGR))

    def saverecord(self, nfile="data.csv"):
        adata=self.data.drop(self.badindx)
        adata.to_csv(nfile)

    def predict(self, indx=0):
        cur_img = self.getImage(indx)
        y_input = cur_img.copy()  # NN input
        pred_throttle, pred_motor = 0.15, 0.15
        if self.servo_model:
            #y = cnn_model.predict([pre])
            pred_throttle = self.servo_model.predict(y_input)

        if self.motor_model:
            #y = cnn_model.predict([pre])
            pred_motor = self.motor_model.predict(y_input)

        return pred_throttle, pred_motor
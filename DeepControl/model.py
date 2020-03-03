from __future__ import print_function, division

import torch
from myNet import SteeringNet, SpeedNet
from torch.autograd import Variable
import torch.nn as nn
import torchvision.transforms.functional as tf

import torch.optim as optim

import numpy as np
import matplotlib.pyplot as plt
import signal
import sys
import os

from dataloader import SimulationDataset
import utils as utils
import csv
csv.field_size_limit(1000000000)

# Surpress traceback in case of user interrupt
signal.signal(signal.SIGINT, lambda x,y: sys.exit(0))

class Struct(object): pass

########################################################################
# Define the network
# ^^^^^^^^^^^^^^^^^^^^


class Model1():    

    ########################################################################
    # Define configuration, log and network instance
    # ^^^^^^^^^^^^^^^^^^^^

    def __init__(self):

        self.input_shape = (utils.IMAGE_HEIGHT, utils.IMAGE_WIDTH)
        
        cfg = Struct()
        cfg.log_dir = "."
        cfg.log_file = "log.json"
        cfg.plot_file = "plot.png"
        cfg.auto_plot = True
        cfg.clean_start = False
        cfg.batch_size = 50
        cfg.test_rate = 10
        cfg.test_epochs = 1
        cfg.train_epochs = 500
        cfg.optimizer = 'adam'
        cfg.cuda = False

        self.cfg = cfg
     #   self.log = Logger(cfg)

        # Clean start 
        if os.path.exists(os.path.join(cfg.log_dir, cfg.log_file)) and cfg.clean_start:
            os.remove(os.path.join(cfg.log_dir, cfg.log_file))

        self.net1 = SteeringNet()
        if (self.cfg.cuda):
            self.net1.cuda()

    ########################################################################
    # Load data
    # ^^^^^^^^^^^^^^^^^^^^
    
    def loadServoData(self, DATA_FILES):


        trainset_servo = SimulationDataset(DATA_FILES, "servo")

        # weights = utils.get_weights(trainset)
        # sampler = torch.utils.data.sampler.WeightedRandomSampler(weights, len(weights), replacement=False)
        # self.trainloader = torch.utils.data.DataLoader(trainset, batch_size=self.cfg.batch_size, sampler=sampler, num_workers=0, pin_memory=True)
        self.trainloader_servo = torch.utils.data.DataLoader(trainset_servo, shuffle=True, batch_size=self.cfg.batch_size, num_workers=0, pin_memory=True)

 #       testset = SimulationDataset("test", transforms=transforms.Compose([
 #               utils.RandomCoose(['center']),
 #               utils.Preprocess(self.input_shape),
 #               utils.ToTensor(),
 #               utils.Normalize([0.1, 0.4, 0.4], [0.9, 0.6, 0.5])
 #           ]))
 #       self.testloader = torch.utils.data.DataLoader(testset, batch_size=self.cfg.batch_size, shuffle=False, num_workers=0, pin_memory=True)

        # Assert trainset and testset are different
        # assert(not bool(set(trainset.__get_samples__()).intersection(testset.__get_samples__())))

    ########################################################################
    # Helper methods
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    # Save model in file system
    def savemodel(self, mfile='servo_model.pth'):
        print('Saving Servo Model ')
        torch.save(self.net1.state_dict(), mfile)

    # Load model from file system
    def loadmodel(self, mfile='servo_model.pth'):
        self.net1.load_state_dict(torch.load(mfile,map_location=lambda storage, loc: storage))
        #self.net.load_state_dict(torch.load(mfile))


    ########################################################################
    # Train the network
    # ^^^^^^^^^^^^^^^^^^^^
    def train(self):

        test_res, tmp_res, best_epoch = 0, 0, 0

        #set train mode
        self.net1.train()

        if (self.cfg.cuda):
            criterion = nn.MSELoss().cuda()
        else:
            criterion = nn.MSELoss()

        if self.cfg.optimizer == 'adam':
            optimizer = optim.Adam(self.net1.parameters(), lr=0.0001)
        elif self.cfg.optimizer == 'adadelta':
            optimizer = optim.Adadelta(self.net1.parameters(), lr=1.0, rho=0.9, eps=1e-06, weight_decay=0)
        else:
            optimizer = optim.SGD(self.net1.parameters(), lr=0.0001, momentum=0.9)
            # optimizer = optim.SGD(self.net.parameters(), lr=0.0001, momentum=0.9, weight_decay=0.01, dampening=0.0)

        total_loss_servo = []
        epoch = 0
        for epoch in range(self.cfg.train_epochs):  # loop over the dataset multiple times

            train_loss_servo, running_loss_servo = 0, 0

            for i, data in enumerate(self.trainloader_servo, 0):
                # get the inputs
                inputs, labels = data
                #print("input and labels values:",inputs,labels)
                # wrap them in Variable
                if (self.cfg.cuda):
                    inputs, labels = Variable(inputs.cuda(non_blocking=True)), Variable(labels.cuda(non_blocking=True))
                else:
                    inputs, labels = Variable(inputs), Variable(labels)

                # zero the parameter gradients
                optimizer.zero_grad()

                # forward + backward + optimize
                if (self.cfg.cuda):
                    outputs = self.net1(inputs).cuda(non_blocking=True)
                else:
                    outputs = self.net1(inputs)

                # Remove one dimension
                outputs = outputs.squeeze()
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()

                running_loss_servo += loss.item()
                del loss

                # print statistics
                if i % 5 == 4:    # print every 5 mini-batches                    
                    print('[%d, %5d] loss: %.6f' % (epoch + 1, i + 1, running_loss_servo / (i+1)))
            
            train_loss_servo = running_loss_servo / len(self.trainloader_servo) 
            print('MSE of the network on the traintset: %.6f' % (train_loss_servo))
            
            total_loss_servo.append(train_loss_servo)
            
            epoch = epoch + 1
        print("servo_dataset training finish!")
        
        x = range(0,epoch)

        total_loss_servo = np.array(total_loss_servo)
        plt.plot(x, total_loss_servo, linewidth = 4, color='r',label="servo")
        plt.show()
        plt.savefig("loss_curve_servo.png")
    ########################################################################
    # Test the network on the test data
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    def test(self):
        # set test mode
        self.net1.eval()

        if (self.cfg.cuda):
            criterion = nn.MSELoss().cuda()
        else:
            criterion = nn.MSELoss()

        test_loss, running_loss = 0, 0

        for epoch in range(self.cfg.test_epochs):  # loop over the dataset multiple times
            for data in self.testloader:
                inputs, labels = data
                if (self.cfg.cuda):
                    inputs, labels = Variable(inputs.cuda(non_blocking=True)), Variable(labels.cuda(non_blocking=True))
                else:
                    inputs, labels = Variable(inputs), Variable(labels)

                if (self.cfg.cuda):
                    outputs = self.net1(inputs).cuda(non_blocking=True)
                else:
                    outputs = self.net1(inputs)

                # Compute mean squared error
                loss = criterion(outputs, labels)
                running_loss += loss.item()
                del loss

        if (self.cfg.test_epochs > 0):
            test_loss = running_loss / (len(self.testloader) * self.cfg.test_epochs) 

        print('MSE of the network on the testset: %.6f' % (test_loss))
        # set train mode
        self.net1.train()

        return test_loss

    ########################################################################
    # Predict control tensor from image
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def predict(self, image, preloaded=False):
        # set test mode
        self.net1.eval()

        if (not preloaded):
            self.loadmodel()

        '''
        composed=transforms.Compose([
            utils.Preprocess(self.input_shape),
            utils.ToTensor(),
            utils.Normalize([0.1, 0.4, 0.4], [0.9, 0.6, 0.5])
        ])
        '''
        # Target gets discareded
        sample = {'image': image, 'target': 0}
        sample["image"] = tf.to_tensor(sample["image"])
        #sample  = composed(sample)
        inputs = sample['image']
        # Add single batch diemension
        inputs = inputs.unsqueeze(0)

        if (self.cfg.cuda):
            inputs = Variable(inputs.cuda(non_blocking=True))
        else:
            inputs = Variable(inputs)

        if (self.cfg.cuda):
            outputs = self.net1(inputs).cuda(non_blocking=True)
        else:
            outputs = self.net1(inputs)

        # print('Control tensor: %.6f ' % (outputs.item()))

        # set train mode
        self.net1.train()

        return outputs.item()

class Model2():    

    ########################################################################
    # Define configuration, log and network instance
    # ^^^^^^^^^^^^^^^^^^^^

    def __init__(self):

        self.input_shape = (utils.IMAGE_HEIGHT, utils.IMAGE_WIDTH)
        
        cfg = Struct()
        cfg.log_dir = "."
        cfg.log_file = "log.json"
        cfg.plot_file = "plot.png"
        cfg.auto_plot = True
        cfg.clean_start = False
        cfg.batch_size = 50
        cfg.test_rate = 10
        cfg.test_epochs = 1
        cfg.train_epochs = 500
        cfg.optimizer = 'adam'
        cfg.cuda = False

        self.cfg = cfg
     #   self.log = Logger(cfg)

        # Clean start 
        if os.path.exists(os.path.join(cfg.log_dir, cfg.log_file)) and cfg.clean_start:
            os.remove(os.path.join(cfg.log_dir, cfg.log_file))

        self.net2 = SpeedNet()
        if (self.cfg.cuda):
            self.net2.cuda()

    ########################################################################
    # Load data
    # ^^^^^^^^^^^^^^^^^^^^
    
    def loadMotorData(self, DATA_FILES):
        
        trainset_motor = SimulationDataset(DATA_FILES, type="motor")
        # weights = utils.get_weights(trainset)
        # sampler = torch.utils.data.sampler.WeightedRandomSampler(weights, len(weights), replacement=False)
        # self.trainloader = torch.utils.data.DataLoader(trainset, batch_size=self.cfg.batch_size, sampler=sampler, num_workers=0, pin_memory=True)
        self.trainloader_motor = torch.utils.data.DataLoader(trainset_motor, shuffle=True, batch_size=self.cfg.batch_size, num_workers=0, pin_memory=True)

 #       testset = SimulationDataset("test", transforms=transforms.Compose([
 #               utils.RandomCoose(['center']),
 #               utils.Preprocess(self.input_shape),
 #               utils.ToTensor(),
 #               utils.Normalize([0.1, 0.4, 0.4], [0.9, 0.6, 0.5])
 #           ]))
 #       self.testloader = torch.utils.data.DataLoader(testset, batch_size=self.cfg.batch_size, shuffle=False, num_workers=0, pin_memory=True)

        # Assert trainset and testset are different
        # assert(not bool(set(trainset.__get_samples__()).intersection(testset.__get_samples__())))

    ########################################################################
    # Helper methods
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    # Save model in file system
    def savemodel(self, mfile='motor_model.pth'):
        print('Saving motor Model ')
        torch.save(self.net2.state_dict(), mfile)

    # Load model from file system
    def loadmodel(self, mfile='motor_model.pth'):
        self.net2.load_state_dict(torch.load(mfile,map_location=lambda storage, loc: storage))
        #self.net.load_state_dict(torch.load(mfile))


    ########################################################################
    # Train the network
    # ^^^^^^^^^^^^^^^^^^^^
    def train(self):

        test_res, tmp_res, best_epoch = 0, 0, 0

        #set train mode
        self.net2.train()

        if (self.cfg.cuda):
            criterion = nn.MSELoss().cuda()
        else:
            criterion = nn.MSELoss()

        if self.cfg.optimizer == 'adam':
            optimizer = optim.Adam(self.net2.parameters(), lr=0.0001)
        elif self.cfg.optimizer == 'adadelta':
            optimizer = optim.Adadelta(self.net2.parameters(), lr=1.0, rho=0.9, eps=1e-06, weight_decay=0)
        else:
            optimizer = optim.SGD(self.net2.parameters(), lr=0.0001, momentum=0.9)
            # optimizer = optim.SGD(self.net.parameters(), lr=0.0001, momentum=0.9, weight_decay=0.01, dampening=0.0)

        total_loss_motor = []
        epoch = 0
        for epoch in range(self.cfg.train_epochs):  # loop over the dataset multiple times

            train_loss_motor, running_loss_motor = 0, 0

            for i, data in enumerate(self.trainloader_motor, 0):
                # get the inputs
                inputs, labels = data
                #print("input and labels values:",inputs,labels)
                # wrap them in Variable
                if (self.cfg.cuda):
                    inputs, labels = Variable(inputs.cuda(non_blocking=True)), Variable(labels.cuda(non_blocking=True))
                else:
                    inputs, labels = Variable(inputs), Variable(labels)

                # zero the parameter gradients
                optimizer.zero_grad()

                # forward + backward + optimize
                if (self.cfg.cuda):
                    outputs = self.net2(inputs).cuda(non_blocking=True)
                else:
                    outputs = self.net2(inputs)

                # Remove one dimension
                outputs = outputs.squeeze()
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()

                running_loss_motor += loss.item()
                del loss

                # print statistics
                if i % 5 == 4:    # print every 5 mini-batches                    
                    print('[%d, %5d] loss: %.6f' % (epoch + 1, i + 1, running_loss_motor / (i+1)))
            epoch = epoch + 1
            print("motor_dataset training finish!")
        
            train_loss_motor = running_loss_motor / len(self.trainloader_motor) 
            print('MSE of the network on the traintset: %.6f' % (train_loss_motor))
            
            total_loss_motor.append(train_loss_motor)
            print("epoch:",epoch)
            '''
            if ((epoch + 1) % self.cfg.test_rate == 0):
                    self.log.logLoss((epoch+1, train_loss))
                    tmp_res = self.test()
                    self.log.logTest((epoch+1, tmp_res))
                    # Check test result over all splits to save best model
                    if (tmp_res < test_res or test_res == 0 or True):
                        self.saveModel()
                        test_res = tmp_res
                        best_epoch = epoch+1
            '''
        print('Finished Training')
        print('Lowest model MSE: %.6f - in epoch: %d' % (test_res, best_epoch))

        x = range(0,epoch)

        total_loss_motor = np.array(total_loss_motor)
        plt.plot(x, total_loss_motor, linewidth = 4, color='b',label="motor")
        plt.show()
        plt.savefig("loss_curve_motor.png")
    ########################################################################
    # Test the network on the test data
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    def test(self):
        # set test mode
        self.net2.eval()

        if (self.cfg.cuda):
            criterion = nn.MSELoss().cuda()
        else:
            criterion = nn.MSELoss()

        test_loss, running_loss = 0, 0

        for epoch in range(self.cfg.test_epochs):  # loop over the dataset multiple times
            for data in self.testloader:
                inputs, labels = data
                if (self.cfg.cuda):
                    inputs, labels = Variable(inputs.cuda(non_blocking=True)), Variable(labels.cuda(non_blocking=True))
                else:
                    inputs, labels = Variable(inputs), Variable(labels)

                if (self.cfg.cuda):
                    outputs = self.net1(inputs).cuda(non_blocking=True)
                else:
                    outputs = self.net1(inputs)

                # Compute mean squared error
                loss = criterion(outputs, labels)
                running_loss += loss.item()
                del loss

        if (self.cfg.test_epochs > 0):
            test_loss = running_loss / (len(self.testloader) * self.cfg.test_epochs) 

        print('MSE of the network on the testset: %.6f' % (test_loss))
        # set train mode
        self.net2.train()

        return test_loss

    ########################################################################
    # Predict control tensor from image
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def predict(self, image, preloaded=False):
        # set test mode
        self.net2.eval()

        if (not preloaded):
            self.loadmodel()
        '''
        composed=transforms.Compose([
            utils.Preprocess(self.input_shape),
            utils.ToTensor(),
            utils.Normalize([0.1, 0.4, 0.4], [0.9, 0.6, 0.5])
        ])
        '''
        # Target gets discareded
        sample = {'image': image, 'target': 0}
        sample["image"] = tf.to_tensor(sample["image"])
        #sample  = composed(sample)
        inputs = sample['image']
        # Add single batch diemension
        inputs = inputs.unsqueeze(0)

        if (self.cfg.cuda):
            inputs = Variable(inputs.cuda(non_blocking=True))
        else:
            inputs = Variable(inputs)

        if (self.cfg.cuda):
            outputs = self.net2(inputs).cuda(non_blocking=True)
        else:
            outputs = self.net2(inputs)

        # print('Control tensor: %.6f ' % (outputs.item()))

        # set train mode
        self.net2.train()

        return outputs.item()

########################################################################
# Main method
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

if  __name__ =='__main__':
    model1 = Model1()
    # model.loadModel()
    DATA_FILES = ['./data24/output_{}.csv'.format(i) for i in range(17)]
    model1.loadServoData(DATA_FILES)
    model1.train()
    model1.savemodel()
           
    
    model2 = Model2()
    #DATA_FILES = ['./data24/output_{}.csv'.format(i) for i in range(17)]
    model2.loadMotorData(DATA_FILES)
    model2.train()
    model2.savemodel()
    
    # image_path = r'C:\Users\patri\Documents\Python Workspace\autonomous_car_simulation\IMG\center_2019_01_23_19_09_22_763.jpg'
    # image = Image.open(image_path)    
    # model.predict(image)

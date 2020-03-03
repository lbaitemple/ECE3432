from __future__ import print_function, division
import torch
import numpy as np
from torch.utils.data import Dataset
import torchvision.transforms.functional as F


import pandas as pd
from scipy.ndimage import gaussian_filter1d

from img_serializer import deserialize_image
class SimulationDataset(Dataset):
    """Dataset wrapping input and target tensors for the driving simulation dataset.

    Arguments:
        set (String):  Dataset - train, test
        path (String): Path to the csv file with the image paths and the target values
    """
    def __init__(self, DATA_FILES, transforms=None, type="servo"):

        self.transforms = transforms
        self.type = type

        #self.data = pd.read_csv(csv_path, error_bad_lines=False)
        # First column contains the middle image paths
        # Fourth column contains the steering angle

#        self.image_paths = np.array(self.data.iloc[start:end, 0:3])
        print('[!] Loading dataset...')
        X = []
        SERVO = []
        
        for d in DATA_FILES:
            print(d)
            c_x, c_servo = self.get_servo_dataset(d)
            X = X + c_x
            SERVO = SERVO + c_servo

        X = np.array(X)
        SERVO = np.array(SERVO) 
        print('[!] Finished loading dataset...')
        
        self.images = X
        self.targets = SERVO

        # Preprocess and filter data
        self.targets = gaussian_filter1d(self.targets, 2)
        # bias = 0.03
        # self.image_paths = [image_path for image_path, target in zip(self.image_paths, self.targets) if
        #                     abs(target) > bias]
        # self.targets = [target for target in self.targets if abs(target) > bias]

    def get_servo_dataset(self, filename, start_index=0, end_index=None, conf='/content/gdrive/My Drive/racecar/settings.json'):
        #    data = pd.DataFrame.from_csv(filename,encoding='utf8')
        # data = pd.read_csv(filename,encoding='utf8',engine='python',error_bad_lines=False)
        data = pd.read_csv(filename,encoding='utf8',engine='python',error_bad_lines=False)

        # Outputs
        x = []

        # Servo ranges from 40-150
        servo = []

        for i in data.index[start_index:end_index]:
            # Don't want noisy data
            #        if data['servo'][i] < 40 or data['servo'][i] > 150:
            #            continue

            # Append
            x.append(deserialize_image(data['image'][i], config=conf))
            servo.append(data[self.type][i])

        return x, servo
    
    def __getitem__(self, index):
        image = self.images[index]
  
        target = self.targets[index]
  
        sample = {'image': image, 'target': target}
        #print("before sample values:",sample["image"])
        
        sample["image"] = F.to_tensor(sample["image"])
        sample["target"] = torch.tensor(float(target))
        # If the transform variable is not empty
        # then it applies the operations in the transforms with the order that it is created.
        '''
        if self.transforms is not None:
            sample["image"] = self.transforms(sample["image"])
            target = sample["target"]
            sample["target"] = torch.tensor(float(target))
        '''
        # plt.imshow(F.to_pil_image(sample['image']))
        # plt.title(str(sample['target']))
        # plt.show()
        #sample = {'image': image, 'target': target}
        #print("last sample values:",sample["image"])
        #print("last label values:",sample["target"])
        return sample['image'], sample['target']

    def __len__(self):
        return len(self.images)


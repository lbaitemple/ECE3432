from torch import nn
import torch.nn.functional as F

class SteeringNet(nn.Module):
    def __init__(self):
        super(SteeringNet, self).__init__()

        self.conv1 = nn.Conv2d(3, 24, 3, stride=(2, 2))
        self.conv2 = nn.Conv2d(24, 36, 3, stride=(2, 2))
        self.conv3 = nn.Conv2d(36, 48, 3)
        self.conv4 = nn.Conv2d(48, 64, 3)
        self.conv5 = nn.Conv2d(64, 10, 3)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(10 * 18 * 30, 10)
        self.fc2 = nn.Linear(10, 1)

    def forward(self, x):
        x = F.elu(self.conv1(x))
        # print("conv1_size:",x.shape)
        x = F.elu(self.conv2(x))
        # print("conv2_size:",x.shape)
        x = F.elu(self.conv3(x))
        # print("conv3_size:",x.shape)
        x = F.elu(self.conv4(x))
        # print("conv4_size:",x.shape)
        x = F.elu(self.conv5(x))
        # print("conv5_size:",x.shape)
        # x = self.drop(x)
        # print("drop_size:",x.shape)
        # print(x.size())
        # x = x.view(-1, 64 * 3 * 10)
        # x = F.elu(self.conv6(x))
        # print("conv6_size:",x.shape)
        # x = F.elu(self.conv7(x))
        #        x = F.elu(self.conv8(x))
        # print("conv7_size:",x.shape)

        # x = F.elu(self.conv9(x))
        # x = x.view(-1, 10 * 3 * 10)

        x = x.view(-1, 10 * 18 * 30)
        x = F.elu(self.fc1(x))
        x = F.elu(self.fc2(x))
        # x = F.elu(self.fc3(x))
        # x = self.fc4(x)
        return x


class SpeedNet(nn.Module):
    def __init__(self):
        super(SpeedNet, self).__init__()

        self.conv1 = nn.Conv2d(3, 24, 3, stride=(2, 2))
        self.conv2 = nn.Conv2d(24, 36, 3, stride=(2, 2))
        self.conv3 = nn.Conv2d(36, 48, 3)
        self.conv4 = nn.Conv2d(48, 64, 3)
        self.conv5 = nn.Conv2d(64, 10, 3)
        self.pool = nn.MaxPool2d(2, 2)
        self.drop = nn.Dropout(p=0.5)
        # self.conv6 = nn.Conv2d(64, 50, 1)
        # self.conv7 = nn.Conv2d(50,  10, 1)

        self.fc1 = nn.Linear(10 * 18 * 30, 10)
        self.fc2 = nn.Linear(10, 1)

    def forward(self, x):
        x = F.elu(self.conv1(x))
        x = F.elu(self.conv2(x))
        x = F.elu(self.conv3(x))
        x = F.elu(self.conv4(x))
        x = F.elu(self.conv5(x))
        # x = F.elu(self.conv6(x))
        # x = F.elu(self.conv7(x))

        x = x.view(-1, 10 * 18 * 30)
        x = F.elu(self.fc1(x))
        x = F.elu(self.fc2(x))

        return x

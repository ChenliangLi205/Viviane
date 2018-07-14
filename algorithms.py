# -*- coding: utf-8 -*-
import torch
from torch.autograd import Variable
import torch.nn.functional as F
import numpy as np


class Network(torch.nn.Module):
    def __init__(self, in_num, hidden_layers, out_num):
        """
        :param in_num: int, neural number of the input layer
        :param hidden_layers: int or list of int, neural number of the hidden layers
        :param out_num:
        """
        super(Network, self).__init__()
        if isinstance(hidden_layers, int): # 单层
            self.input_layer = torch.nn.Linear(in_num, hidden_layers)
            self.output_layer = torch.nn.Linear(hidden_layers, out_num)
            self.deep = False

        if isinstance(hidden_layers, list): # 多层
            self.input_layer = torch.nn.Linear(in_num, hidden_layers[0])
            self.hidden_layer = [torch.nn.Linear(hidden_layers[i], hidden_layers[i+1])
                                 for i in range(len(hidden_layers)-1)]
            self.output_layer = torch.nn.Linear(hidden_layers[-1], out_num)
            self.deep = True

    def forward(self, input_x):
        x = F.relu(self.input_layer(input_x))
        if self.deep:
            for hl in self.hidden_layer:
                x = F.relu(hl(x))
        x = F.softmax(self.output_layer(x))
        return x

    def update(self, input_data, target, lr=1e-1, momentum=.9, MAX_ITERS=20):
        """
        更新网络的各种参数
        :param input_data: 输入层数据
        :param target: 训练目标
        :param lr: 学习率
        :param momentum: 学习率的加速度
        :param MAX_ITERS: 最大迭代次数
        """
        loss_function = torch.nn.NLLLoss()  # The negative log likelihood loss
        optimizer = torch.optim.SGD(self.parameters(), lr=lr, momentum=momentum)
        for i in range(MAX_ITERS):
            out = self(input_data)
            loss = loss_function(out, target)
            print("loss is %f" % loss.data.numpy())
            optimizer.zero_grad()  # clear the grad buffers
            loss.backward()
            optimizer.step()  # Do the update

if __name__ == '__main__':
    pass

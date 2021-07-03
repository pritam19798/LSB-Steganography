import cv2
import numpy as np
import random
from error import ImageNotFoundError, DataOverflowError
from message import Message


class LSB(object):

    def __init__(self, img_path, use_channel=3):
        self.img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
        self.use_channel = use_channel
        if self.img is None:
            raise ImageNotFoundError("Sorry, no Image found")
        self.row, self.col, self.channel = self.img.shape[0], self.img.shape[1], self.img.shape[2]
        print(self.row, self.col)

    def hide(self, binary_list):
        msg_iterator = 0
        use_channel = min(self.use_channel, self.channel)
        print(use_channel)
        self.img[0, 0, 0] = len(binary_list)
        while msg_iterator < len(binary_list):
            for row in range(self.row):
                for col in range(self.col):

                    Chanel_block = self.img[row, col]
                    itr_chanel = 0
                    while itr_chanel < use_channel and msg_iterator < len(binary_list):
                        if binary_list[msg_iterator] == 1:
                            if Chanel_block[itr_chanel] % 2 == 0:
                                Chanel_block[itr_chanel] += 1
                        else:
                            if Chanel_block[itr_chanel] % 2 == 1:
                                Chanel_block[itr_chanel] -= 1

                        msg_iterator += 1
                        itr_chanel += 1
                    # print(Chanel_block)
                    self.img[row, col] = Chanel_block
            print(msg_iterator, len(binary_list))
            if msg_iterator < len(binary_list):
                raise DataOverflowError('data overflow!!')
            if msg_iterator >= len(binary_list):
                break
        return self.img

    def show(self):
        binary_list = []

        use_channel = min(self.use_channel, self.channel)

        for row in range(self.row):
            for col in range(self.col):

                Chanel_block = self.img[row, col]
                itr_chanel = 0
                while itr_chanel < use_channel:
                    binary_list.append(Chanel_block[itr_chanel] % 2)
                    itr_chanel += 1

        return binary_list




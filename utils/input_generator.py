import numpy as np
import cv2
import random
from glob import glob

from keras.utils import to_categorical

class InputGenerator(object):
    def  __init__(self,
                datapath,
                input_size,
                augmentation = {
                    "gray_scale": .0,
                    "flip_vertical":.5,
                }
            ):
        dir_list = glob(datapath + '/*.jpg')

        data = []
        # Create shapes
        for path in dir_list:
            filename = path.split('/')[-1]
            speed, dir, _  = filename.split('_')
            data.append([path, (speed, dir)])

        self.data = data
        self.size = len(data)
        self.input_size = input_size

        self.__dict__.update(augmentation)

    def augGrayScale(self, input):
        # ton code ici
        input = np.dot(input[...,:3], [0.299, 0.587, 0.114])
        input = np.reshape(input, (input.shape[0], input.shape[1], 1))
        input = np.concatenate((input, input, input), axis=2)

        cv2.imshow('image',np.uint8(input))
        cv2.waitKey(0)

        return input

    def augFlipVertical(self, input, output):
        pass
        # ton code ici
        return input, output

    def augmentation(self, input, output):
        if random.random() > self.gray_scale:
            input = self.augGrayScale(input)
        if random.random() > self.flip_vertical:
            input, output = self.augFlipVertical(input, output)
        return input, output

    def generator(self, batch_size=32):

        data_copy = self.data.copy()
        random.shuffle(data_copy)

        while True:
            if len(data_copy) < batch_size:
                data_copy = self.data.copy()
                random.shuffle(data_copy)
            X = []
            y = {"fc_speed": [], "fc_direction": []}
            for _ in range(batch_size):
                input_path, output = data_copy[0]
                # Input formating
                input = cv2.imread(input_path)

                """ Data augmentation there
                """
                input, output = self.augmentation(input, output)

                # Normalization
                size = (self.input_size[1], self.input_size[0])
                input = cv2.resize(input, size)
                input = np.float32(input)
                input /= 255.

                # Output formating
                speed, direction = output
                speed, direction = to_categorical(speed, 2), to_categorical(direction, 5)

                X.append(input)
                y['fc_speed'].append(speed)
                y['fc_direction'].append(direction)
                del data_copy[0]

            X = np.array(X)
            y['fc_speed'] = np.array(y['fc_speed'])
            y['fc_direction'] = np.array(y['fc_direction'])
            yield X, y


if __name__ == "__main__":

    gen = InputGenerator("./datas/Train", (96, 160, 3))
    for _ in gen.generator():
        pass

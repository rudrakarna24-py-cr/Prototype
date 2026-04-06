import os
import cv2
import numpy as np

from dense import NeuralNet


def preprocess_image(image_path):
    
    img = cv2.imread(image_path)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img = cv2.resize(img, (64, 64))

    img = img / 255.0

    img = img.reshape(64, 64)

    return img

class ConvLayer:
    def __init__(self, num_filters=8, filter_size=3):
        self.num_filters = num_filters
        self.filter_size = filter_size
        self.filters = np.random.randn(num_filters, filter_size, filter_size) * 0.1

    def forward(self, image):
        self.last_input = image
        h, w = image.shape
        output = np.zeros((h-2, w-2, self.num_filters))

        for f in range(self.num_filters):
            for i in range(h-2):
                for j in range(w-2):
                    region = image[i:i+3, j:j+3]
                    output[i, j, f] = np.sum(region * self.filters[f])

        return output
    

class MaxPool:
    def forward(self, input):
        self.last_input = input
        h, w, f = input.shape
        output = np.zeros((h//2, w//2, f))

        for k in range(f):
            for i in range(0, h, 2):
                for j in range(0, w, 2):
                    region = input[i:i+2, j:j+2, k]
                    output[i//2, j//2, k] = np.max(region)

        return output

class SimpleCNN:
    def __init__(self):
        self.conv = ConvLayer(8, 3)
        self.pool = MaxPool()

        # After conv(64->62) + pool(62->31)
        self.fc = NeuralNet(input_size=31*31*8, h1=64, h2=32, output_size=3)

    def forward(self, image):
        out = self.conv.forward(image)
        out = np.maximum(0, out) # ReLU
        out = self.pool.forward(out)

        out = out.reshape(-1, 1)
        return self.fc.forward(out)
    
    def save_conv(self, filename):
        np.save(filename, self.conv.filters)

    def load_conv(self, filename):
        self.conv.filters = np.load(filename)
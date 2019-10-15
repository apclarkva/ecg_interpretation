import numpy as np
from tensorflow import keras
from keras.models import *
from keras.layers import *
from keras.optimizers import *


def autoencoder(pretrained_weights=None, input_size=(5000, 12)):
    inputs = Input(input_size)

    

    # Encoder
    conv1_1 = Conv2D(16, (3, 3), activation='relu', padding='same')(x)
    pool1 = MaxPooling2D((2, 2), padding='same')(conv1_1)
    conv1_2 = Conv2D(8, (3, 3), activation='relu', padding='same')(pool1)
    pool2 = MaxPooling2D((2, 2), padding='same')(conv1_2)
    conv1_3 = Conv2D(8, (3, 3), activation='relu', padding='same')(pool2)
    h = MaxPooling2D((2, 2), padding='same')(conv1_3)


    # Decoder
    conv2_1 = Conv2D(8, (3, 3), activation='relu', padding='same')(h)
    up1 = UpSampling2D((2, 2))(conv2_1)
    conv2_2 = Conv2D(8, (3, 3), activation='relu', padding='same')(up1)
    up2 = UpSampling2D((2, 2))(conv2_2)
    conv2_3 = Conv2D(16, (3, 3), activation='relu')(up2)
    up3 = UpSampling2D((2, 2))(conv2_3)
    r = Conv2D(1, (3, 3), activation='sigmoid', padding='same')(up3)


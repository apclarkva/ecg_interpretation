import numpy as np
#from tensorflow import keras
from keras.models import *
from keras.layers import *
from keras.optimizers import *
import pandas as pd
import numpy as np
from os import listdir

class Models():
    """
    A Class for creating all ML models
    """

    def __init__(self, path_to_data, model_name='autoencoder', t_span=4096):
        self.signal_length = int(t_span/2)
        self.input_shape = Input(shape=(self.signal_length,2))
        self.path_to_data = path_to_data

        self.input_data = np.array([])
        self.current_model = []

    def format_input_data(self):
        file_names = listdir(self.path_to_data)
        
        self.input_data = np.zeros((len(file_names)*100, self.signal_length, 12))

        index = 0
        for i in range(0, 100):
            for file_name in file_names:
                current_path = f'{self.path_to_data}/{file_name}'
                current_data = np.loadtxt(current_path, skiprows=1, delimiter=',')

                self.input_data[index, :, :] = current_data[0:self.signal_length, :]
                index += 1
                print(index)


    def get_autoencoder(self):
        input_shape = self.input_shape

        #encoder
        conv_e1 = Conv1D(32, 4, activation='relu', padding='same')(
            input_shape)
        pool_e1 = MaxPooling1D(4, padding='same')(conv_e1)

        conv_e2 = Conv1D(64, 4, activation='relu', padding='same')(
            pool_e1)
        pool_e2 = MaxPooling1D(4, padding='same')(conv_e2)

        conv_e3 = Conv1D(128, 2, activation='relu', padding='same')(
            pool_e2)
        pool_e3 = MaxPooling1D(2, padding='same')(conv_e3)

        conv_e4 = Conv1D(512, 2, activation='relu', padding='same')(
            pool_e3)
        low_dim = MaxPooling1D(8, padding='same')(conv_e4)

        # Decoder
        conv_d4 = Conv1D(512, 2, activation='relu', padding='same')(low_dim)
        up4 = UpSampling1D(8)(conv_d4)

        conv_d3 = Conv1D(128, 2, activation='relu', padding='same')(up4)
        up3 = UpSampling1D(2)(conv_d3)

        conv_d2 = Conv1D(64, 4, activation='relu', padding='same')(up3)
        up2 = UpSampling1D(4)(conv_d2)

        conv_d1 = Conv1D(32, 4, activation='relu', padding='same')(up2)
        up1 = UpSampling1D(4)(conv_d1)

        rec_signal = Conv1D(2, 3, activation='sigmoid', padding='same')(up1)

        autoencoder = Model(input=input_shape, output=rec_signal)
        autoencoder.compile(optimizer='adam', loss='mse')

        self.current_model = autoencoder


    def get_small_autoencoder(self):
        input_shape = self.input_shape

        #encoder
        conv_e1 = Conv1D(32, 4, activation='relu', padding='same')(
            input_shape)
        conv_e1_2 = Conv1D(64, 4, activation='relu', padding='same')(
            conv_e1)
        pool_e1 = MaxPooling1D(2, padding='same')(conv_e1_2)

        conv_d1 = Conv1D(32, 4, activation='relu', padding='same')(pool_e1)
        up1 = UpSampling1D(2)(conv_d1)

        rec_signal = Conv1D(12, 3, activation='sigmoid', padding='same')(up1)

        autoencoder = Model(input=input_shape, output=rec_signal)
        autoencoder.compile(optimizer='adam', loss='mse')

        self.current_model = autoencoder

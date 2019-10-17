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

    def __init__(self, path_to_data, model_name='autoencoder', t_span=4096, num_channels=12):
        self.signal_length = int(t_span/2)
        self.input_shape = Input(shape=(self.signal_length,num_channels))
        self.path_to_data = path_to_data
        self.num_channels = num_channels

        self.input_data = np.array([])
        self.current_model = []

    def format_input_data(self):
        file_names = listdir(self.path_to_data)
        
        self.input_data = np.zeros((len(file_names)*100, self.signal_length, self.num_channels))

        index = 0
        for i in range(0, 100):
            for file_name in file_names:
                current_path = f'{self.path_to_data}/{file_name}'
                current_data = np.loadtxt(current_path, skiprows=1, delimiter=',')

                self.input_data[index, :, :] = current_data[0:self.signal_length, :]
                index += 1
                print(index)

    def load_from_npy(self, directory_path, num_files=100):
        file_names = listdir(directory_path)

        if len(file_names) > num_files:
            file_names = file_names[0:num_files]

        self.input_data = np.zeros((len(file_names), self.signal_length, self.num_channels))
        index = 0
        for file_name in file_names:
            current_path = f'{self.path_to_data}/{file_name}'
            current_signal = np.load(current_path)
            current_signal = self._norm_signal_channels(current_signal)
            self.input_data[index, :, :] = current_signal[0:self.signal_length, 0:self.num_channels]
            print(index)
            index+=1
    
    def _norm_signal_channels(self, signal_all_channels):
        return np.apply_along_axis(self._norm_column, 0, signal_all_channels)

    def _norm_column(self, signal):
        if signal.min() > 0:
            positive_signal = signal - signal.min()
        else:
            positive_signal = signal + np.abs(signal.min())
        normalized_signal = positive_signal / positive_signal.max()
        return normalized_signal

    def get_autoencoder(self):
        input_shape = self.input_shape

        #encoder
        #1
        conv_e1 = Conv1D(64, 4, activation='relu', padding='same')(
            input_shape)
        pool_e1 = MaxPooling1D(2, padding='same')(conv_e1)

        #2
        conv_e2 = Conv1D(128, 4, activation='relu', padding='same')(
            pool_e1)
        pool_e2 = MaxPooling1D(2, padding='same')(conv_e2)

        #3
        conv_e3 = Conv1D(256, 9, activation='relu', padding='same')(
            pool_e2)
        pool_e3 = MaxPooling1D(2, padding='same')(conv_e3)

        #4
        conv_e4 = Conv1D(512, 9, activation='relu', padding='same')(
            pool_e3)
        pool_e4= MaxPooling1D(2, padding='same')(conv_e4)

        #5
        conv_e5 = Conv1D(512, 6, activation='relu', padding='same')(
            pool_e4)
        conv_e5_2 = Conv1D(256, 8, activation='relu', padding='same')(
            conv_e5)
        pool_e5 = MaxPooling1D(2, padding='same')(conv_e5_2)

        #6
        conv_e6 = Conv1D(512, 12, activation='relu', padding='same')(
            pool_e5)
        conv_e6_2 = Conv1D(256, 5, activation='relu', padding='same')(
            conv_e6)
        pool_e6 = MaxPooling1D(2, padding='same')(conv_e6_2)

        #7
        conv_e7 = Conv1D(128, 4, activation='relu', padding='same')(
            pool_e6)
        conv_e7_2 = Conv1D(128, 2, activation='relu', padding='same')(
            conv_e7)


        low_dim = MaxPooling1D(2, padding='same')(conv_e7_2)


        # Decoder
        #7
        conv_d7 = Conv1D(128, 2, activation='relu', padding='same')(
            low_dim)
        conv_d7_2 = Conv1D(128, 4, activation='relu', padding='same')(
            conv_d7)
        up7 = UpSampling1D(2)(conv_d7_2)

        #6
        conv_d6 = Conv1D(256, 5, activation='relu', padding='same')(up7)
        conv_d6_2 = Conv1D(512, 12, activation='relu', padding='same')(conv_d6)
        up6 = UpSampling1D(2)(conv_d6_2)

        #5
        conv_d5 = Conv1D(256, 8, activation='relu', padding='same')(up6)
        conv_d5_2 = Conv1D(512, 6, activation='relu', padding='same')(conv_d5)
        up5 = UpSampling1D(2)(conv_d5_2)

        #4
        conv_d4 = Conv1D(512, 9, activation='relu', padding='same')(up5)
        up4 = UpSampling1D(2)(conv_d4)

        #3
        conv_d3 = Conv1D(256, 9, activation='relu', padding='same')(up4)
        up3 = UpSampling1D(2)(conv_d3)

        #2
        conv_d2 = Conv1D(128, 4, activation='relu', padding='same')(up3)
        up2 = UpSampling1D(2)(conv_d2)

        #1
        conv_d1 = Conv1D(64, 4, activation='relu', padding='same')(up2)
        up1 = UpSampling1D(2)(conv_d1)

        #out
        rec_signal = Dense(12, activation='sigmoid')(up1)

        autoencoder = Model(input=input_shape, output=rec_signal)
        autoencoder.compile(optimizer='adam', loss='mse')

        self.current_model = autoencoder


    def get_small_autoencoder(self):
        input_shape = self.input_shape

        #encoder
        #1
        conv_e1 = Conv1D(32, 20, activation='relu', padding='same')(
            input_shape)
        pool_e1 = MaxPooling1D(2, padding='same')(conv_e1)

        #2
        conv_e2 = Conv1D(64, 4, activation='relu', padding='same')(
            pool_e1)
        conv_e2_2 = Conv1D(64, 4, activation='relu', padding='same')(
            conv_e2)
        pool_e2 = MaxPooling1D(2, padding='same')(conv_e2_2)

        #3
        conv_e3 = Conv1D(32, 4, activation='relu', padding='same')(
            pool_e2)
        conv_e3_2 = Conv1D(32, 4, activation='relu', padding='same')(
            conv_e3)
        pool_e3 = MaxPooling1D(2, padding='same')(conv_e3_2)


        #3
        conv_d3 = Conv1D(32, 4, activation='relu', padding='same')(pool_e3)
        conv_d3_2 = Conv1D(32, 4, activation='relu', padding='same')(conv_d3)
        up3 = UpSampling1D(2)(conv_d3_2)

        #2 
        conv_d2_2 = Conv1D(64, 4, activation='relu', padding='same')(up3)
        conv_d2 = Conv1D(32, 30, activation='relu', padding='same')(conv_d2_2)
        up2 = UpSampling1D(2)(conv_d2)

        #1
        conv_d1 = Conv1D(32, 4, activation='relu', padding='same')(up2)
        up1 = UpSampling1D(2)(conv_d1)

        #out
        rec_signal = Dense(12, activation='sigmoid')(up1)

        autoencoder = Model(input=input_shape, output=rec_signal)
        autoencoder.compile(optimizer='adam', loss='mse')

        self.current_model = autoencoder





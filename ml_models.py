import numpy as np
from keras.models import *
from keras.layers import *
from keras.optimizers import *
import numpy as np
from os import listdir
import random
try:
    import matplotlib.pyplot as plt
except:
    print('no matplotlib')
try:
    from sklearn.decomposition import PCA
except: 
    print('no sklearn')
try:
    import pandas as pd
except: 
    print('no pandas')



class Models():
    """
    A Class for creating all ML models
    """

    def __init__(self, model_name='autoencoder',
                 slices=3, num_channels=12, test_proportion=.8, 
                 ecg_time_samples=5000):
        self.signal_length = int(ecg_time_samples/slices)
        self.slices = slices
        self.input_shape = Input(shape=(self.signal_length,num_channels))
        self.num_channels = num_channels
        self.test_proportion = test_proportion

        self.normal_training = np.array([])
        self.normal_testing = np.array([])
        self.afib_data = np.array([])
        self.current_model = []
        self.encoder = []
        self.norm_predict = []
        self.history = []

    def load_data(self, path_to_data ,num_files=100, rhythm_type='normal'):
        file_names = listdir(path_to_data)

        if len(file_names) > num_files:
            file_names = file_names[0:num_files]

        input_data = np.zeros((len(file_names)*self.slices,
                               self.signal_length,
                               self.num_channels))

        index = 0
        for file_name in file_names:
            current_path = f'{path_to_data}/{file_name}'
            current_signal = np.load(current_path)
            current_signal = self._norm_signal_channels(current_signal)
            for num in range(self.slices):
                input_data[index, :, :] = current_signal[0:self.signal_length,
                                                         0:self.num_channels]
                index+=1

        num_training = round(num_files * self.slices * self.test_proportion)
        if rhythm_type == 'normal': 
            self.normal_training = input_data[0:num_training, :, :]
            self.normal_testing = input_data[num_training:, :, :]
        if rhythm_type == 'afib':
            self.afib_data = input_data
    
    def _norm_signal_channels(self, signal_all_channels):
        return np.apply_along_axis(self._norm_column, 0, signal_all_channels)

    def _norm_column(self, signal):
        if signal.min() > 0:
            positive_signal = signal - signal.min()
        else:
            positive_signal = signal + np.abs(signal.min())
        normalized_signal = positive_signal / positive_signal.max()
        return normalized_signal

    def get_100x_autoencoder(self):
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

        #4
        conv_e4 = Conv1D(32, 4, activation='relu', padding='same')(
            pool_e3)
        conv_e4_2 = Conv1D(16, 4, activation='relu', padding='same')(
            conv_e4)
        pool_e4 = MaxPooling1D(2, padding='same')(conv_e4_2)

        #5
        conv_e5 = Conv1D(16, 4, activation='relu', padding='same')(
            pool_e4)
        conv_e5_2 = Conv1D(8, 4, activation='relu', padding='same')(
            conv_e5)
        pool_e5 = MaxPooling1D(2, padding='same')(conv_e5_2)

        #6
        conv_e6 = Conv1D(16, 4, activation='relu', padding='same')(
            pool_e5)
        conv_e6_2 = Conv1D(8, 4, activation='relu', padding='same')(
            conv_e6)
        pool_e6 = MaxPooling1D(2, padding='same')(conv_e6_2)


        #6
        conv_d6 = Conv1D(8, 4, activation='relu', padding='same')(pool_e6)
        conv_d6_2 = Conv1D(16, 4, activation='relu', padding='same')(conv_d6)
        up6 = UpSampling1D(2)(conv_d6_2)

        #5
        conv_d5 = Conv1D(8, 4, activation='relu', padding='same')(up6)
        conv_d5_2 = Conv1D(16, 4, activation='relu', padding='same')(conv_d5)
        up5 = UpSampling1D(2)(conv_d5_2)


        #4
        conv_d4 = Conv1D(16, 4, activation='relu', padding='same')(up5)
        conv_d4_2 = Conv1D(32, 4, activation='relu', padding='same')(conv_d4)
        up4 = UpSampling1D(2)(conv_d4_2)


        #3
        conv_d3 = Conv1D(32, 4, activation='relu', padding='same')(up4)
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

    def get_50x_autoencoder(self):
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

        #4
        conv_e4 = Conv1D(32, 4, activation='relu', padding='same')(
            pool_e3)
        conv_e4_2 = Conv1D(16, 4, activation='relu', padding='same')(
            conv_e4)
        pool_e4 = MaxPooling1D(2, padding='same')(conv_e4_2)

        #5
        conv_e5 = Conv1D(16, 4, activation='relu', padding='same')(
            pool_e4)
        conv_e5_2 = Conv1D(8, 4, activation='relu', padding='same')(
            conv_e5)
        pool_e5 = MaxPooling1D(2, padding='same')(conv_e5_2)


        #5
        conv_d5 = Conv1D(8, 4, activation='relu', padding='same')(pool_e5)
        conv_d5_2 = Conv1D(16, 4, activation='relu', padding='same')(conv_d5)
        up5 = UpSampling1D(2)(conv_d5_2)


        #4
        conv_d4 = Conv1D(16, 4, activation='relu', padding='same')(up5)
        conv_d4_2 = Conv1D(32, 4, activation='relu', padding='same')(conv_d4)
        up4 = UpSampling1D(2)(conv_d4_2)


        #3
        conv_d3 = Conv1D(32, 4, activation='relu', padding='same')(up4)
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

    def get_10x_autoencoder(self):
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

        #4
        conv_e4 = Conv1D(32, 4, activation='relu', padding='same')(
            pool_e3)
        conv_e4_2 = Conv1D(16, 4, activation='relu', padding='same')(
            conv_e4)
        pool_e4 = MaxPooling1D(2, padding='same')(conv_e4_2)


        #4
        conv_d4 = Conv1D(32, 4, activation='relu', padding='same')(pool_e4)
        conv_d4_2 = Conv1D(32, 4, activation='relu', padding='same')(conv_d4)
        up4 = UpSampling1D(2)(conv_d4_2)


        #3
        conv_d3 = Conv1D(32, 4, activation='relu', padding='same')(up4)
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

    def get_3x_autoencoder(self):
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

    def get_encoder(self):
        encoded_layer = self.current_model.layers[int(len(self.current_model.layers)/2)]
        self.encoder = Model(self.current_model.inputs, encoded_layer.output)

    def get_error_by_input(self):
        try:
            self.norm_errors = self._return_all_errors(self.normal_testing)
        except:
            print('Could not get normal testing errors')
        try:
            self.afib_errors = self._return_all_errors(self.afib_data)
        except:
            print('Could not get afib testing errors')

    def _return_all_errors(self, input_data):
        test_error = np.zeros(len(input_data[:, 0, 0]))
        for i in range(0, len(test_error)):
            current_input = np.expand_dims(input_data[i,:,:], axis=0)
            test_error[i] = self.current_model.evaluate(current_input, current_input)

        return test_error

    def load_existing_model(self, file_name):
        self.current_model = load_model(file_name)

    def run_autoencoder(self, val_split=.2, n_batch=32, n_epochs=100):
        self.history = self.current_model.fit(self.normal_training,
                                              self.normal_training,
                                              validation_split=val_split,
                                              verbose=1,
                                              batch_size=n_batch,
                                              epochs=n_epochs)

    def plot_history(self):
        if not self.history:
            return

        try:
            import matplotlib.pyplot as plt
            history = self.history

            plt.plot(history.history['loss'])
            plt.plot(history.history['val_loss'])
            plt.title('Model Loss')
            plt.ylabel('Loss')
            plt.xlabel('Epoch')
            plt.legend(['Train', 'Test'], loc='upper left')
            plt.show()
        except:
            print('Could not plot loss')

    def evaluate_model(self):
        if not self.history:
            return

        self.norm_eval = self.current_model.evaluate(self.normal_testing,
                                                     self.normal_testing)
        self.afib_eval = self.current_model.evaluate(self.afib_data,
                                                     self.afib_data)

    def predict_test_data(self, is_plotted=False, n_bin=40, n_range=.02):
        if not self.norm_predict:
            self.norm_predict = self.current_model.predict(self.normal_testing)
            self.afib_predict = self.current_model.predict(self.afib_data)

        if is_plotted:
            plt.hist(self.norm_errors,
                     bins=n_bin, alpha=0.5, range=(0, n_range))
            plt.hist(self.afib_errors,
                     bins=n_bin, alpha=0.5, range=(0, n_range))
            plt.show()


    def encode_data(self):
        encoder = self.encoder

        norm_encoded = encoder.predict(self.normal_testing)
        num_obs = len(norm_encoded[:,0,0])
        num_cols = len(norm_encoded[0,:,0])*len(norm_encoded[0,0,:])
        self.norm_encoded_flat = norm_encoded.reshape(
            (num_obs, num_cols), order='f')

        afib_encoded = encoder.predict(self.afib_data)
        num_obs = len(afib_encoded[:,0,0])
        num_cols = len(afib_encoded[0,:,0])*len(norm_encoded[0,0,:])
        self.afib_encoded_flat = afib_encoded.reshape(
            (num_obs, num_cols), order='f')

    def get_pca_encoded(self, is_plotted=False):
        pca_inputs = np.concatenate((self.norm_encoded_flat, 
                                     self.afib_encoded_flat))
        pca = PCA(n_components=12)
        components = pca.fit_transform(pca_inputs)

        if is_plotted:
            import pdb
            pdb.set_trace()
            num_normal = len(self.norm_encoded_flat[:,0])
            plt.scatter(components[0:num_normal,0], components[0:num_normal,1])
            plt.scatter(components[num_normal:,0], components[num_normal:,1])
            plt.show()

        return components


    def plot_random_test_wave(self, wave_type='normal'):
        rand_num = random.random()
        if wave_type == 'normal':
            rand_num = int(len(self.normal_testing[:,0,0])*rand_num)
            original_wave = self.normal_testing[rand_num,:,:] 
            autoencoded_wave = self.norm_predict[rand_num,:,:]
        elif wave_type == 'afib':
            rand_num = int(len(self.afib_data[:,0,0])*rand_num)
            original_wave = self.afib_data[rand_num,:,:]
            autoencoded_wave = self.afib_predict[rand_num,:,:]
        else:
            return

        self.plot_twelve_lead(pd.DataFrame(original_wave),
                              pd.DataFrame(autoencoded_wave))
        
    def plot_twelve_lead(self, original, prediction):
        original.plot(subplots=True,
                            layout=(6, 2),
                            figsize=(6, 6),
                            sharex=False,
                            sharey=False,
                            legend=False,
                            style=['k' for i in range(12)])
        axes = plt.gcf().get_axes()
        index = 0
        for ax in axes:
            prediction.iloc[:,index].plot(ax=ax, style='b')
            ax.axis('off')
            index+=1
            
        plt.show()



from ml_models import Models
import numpy as np
import os
#import matplotlib.pyplot as plt
import pandas as pd
os.environ['KMP_DUPLICATE_LIB_OK']='True'


def main():
    path_to_signals = 'data/ecg/normal_pickled_ind'
    model_obj = Models(path_to_signals, t_span=2048, num_channels=12)

    num_obs = 1200
    model_obj.load_from_npy(path_to_signals, num_obs)
 
    model_obj.get_autoencoder()
    model_obj.current_model.summary()

    autoencoder = model_obj.current_model
        
    history = autoencoder.fit(model_obj.input_data, model_obj.input_data, validation_split=.25, verbose=1, batch_size=300, epochs=50)
    #plot_history(history)
    model_obj.load_from_npy(path_to_signals, (num_obs + 10))
    x_test = model_obj.input_data[num_obs:(num_obs+9), :, :]
    print(autoencoder.evaluate(x_test, x_test))
    x_predict = autoencoder.predict(x_test)

    #plt.plot(x_test[1,:,0])
    #plt.plot(x_predict[1,:,0])
    #plt.show()

    #import pdb
    #pdb.set_trace()









#def plot_against(autoencoder, x_values):
#    x_predict = autoencoder.predict(x_values)
#
#    plt.plot(x_values[0,:,1])
#    plt.plot(x_predict[0,:,1])
#    plt.show()
#
#
#def plot_history(history):
#    plt.plot(history.history['loss'])
#    plt.plot(history.history['val_loss'])
#    plt.title('model loss')
#    plt.ylabel('loss')
#    plt.xlabel('epoch')
#    plt.legend(['train', 'test'], loc='upper left')
#    plt.show()





if __name__ == '__main__':
    main()

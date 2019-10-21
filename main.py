from ml_models import Models
import numpy as np
import os
#import matplotlib.pyplot as plt
import pandas as pd
from keras.models import load_model
os.environ['KMP_DUPLICATE_LIB_OK']='True'


def main():
    model_obj = Models(t_span=2048, num_channels=12)
    num_obs = 7000

    #Data
    path_to_afibs = 'data/ecg/afib_pickled_ind'
    path_to_normals = 'data/ecg/normal_pickled_ind'
    model_obj.load_data(path_to_normals, num_obs, rhythm_type='normal')
    model_obj.load_data(path_to_afibs, num_files=300, rhythm_type='afib')

    #Setup
    model_obj.get_50x_autoencoder()
    model_obj.current_model.summary()
        
    #Run
    model_obj.run_autoencoder(n_epochs=400)

    #Calculate performance
    model_obj.get_error_by_input()
    model_obj.evaluate_model()
    model_obj.predict_test_data()

    print(f'Evaluation of normal data is {model_obj.norm_eval}')
    print(f'Evaluation of afib data is {model_obj.afib_eval}')


    #encoder stuff
    model_obj.get_encoder()
    model_obj.encode_data()
    #model_obj.get_pca_encoded(is_plotted=True)

    model_obj.current_model.save('./data/auto_10x_4000obs.h5')
    
    #plotting
    #model_obj.plot_history()
    #model_obj.plot_random_test_wave('normal')
    #model_obj.plot_random_test_wave('afib')

if __name__ == '__main__':
    main()

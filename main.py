from ml_models import Models
import numpy as np
import os
#import matplotlib.pyplot as plt
from keras.models import load_model
os.environ['KMP_DUPLICATE_LIB_OK']='True'


def load_main():
    num_obs = 700
    num_slices = 1
    model_obj = Models(slices=num_slices, num_channels=12)

    #Data
    path_to_afibs = 'data/ecg/afib_pickled_ind'
    path_to_normals = 'data/ecg/normal_pickled_ind'
    model_obj.normal_training = []
    model_obj.load_data(path_to_normals, num_obs, rhythm_type='normal')
    model_obj.load_data(path_to_afibs, num_files=300, rhythm_type='afib')

    model_obj.current_model =  load_model('./data/model_results/auto_400x_9500obs_1slices_2200epochs_gpu_2/auto_400x_9500obs_1slices_2200epochs_gpu_2.h5')

    #Calculate performance
    model_obj.get_error_by_input()
    model_obj.evaluate_model()
    model_obj.predict_test_data(is_plotted=True)

    model_obj.get_roc_curve()
    model_obj.get_auprc()
    print(f'Evaluation of normal data is {model_obj.norm_eval}')
    print(f'Evaluation of afib data is {model_obj.afib_eval}')
    import pdb
    pdb.set_trace()

    #plotting
    model_obj.plot_random_test_wave('normal')
    model_obj.plot_random_test_wave('afib')

def main():
    num_obs = 15
    num_epochs = 700
    num_slices = 3 
    model_obj = Models(slices=num_slices, num_channels=12)
    
    # Data
    path_to_afibs = 'data/ecg/afib_pickled_ind'
    path_to_normals = 'data/ecg/normal_pickled_ind'
    model_obj.load_data(path_to_normals, num_obs, rhythm_type='normal')
    model_obj.load_data(path_to_afibs, num_files=300, rhythm_type='afib')

    #Setup
    model_obj.get_100x_autoencoder()
    model_obj.current_model.summary()
        
    #Run
    model_obj.run_autoencoder(n_epochs=num_epochs)

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

    model_obj.current_model.save(f'./data/auto_100x_{num_obs}obs_{num_slices}ms_{num_epochs}epochs.h5')
    
    #plotting
    #model_obj.plot_history()
    model_obj.plot_random_test_wave('normal')
    model_obj.plot_random_test_wave('afib')

if __name__ == '__main__':
    load_main()

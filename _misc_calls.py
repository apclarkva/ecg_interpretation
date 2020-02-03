from ml_models import *


num_norms = 10
num_afibs = 10
num_epochs = 1
num_slices = 1 
model_obj = Models()

path_to_afibs = 'data/ecg/afib_pickled_ind'
path_to_normals = 'data/ecg/normal_pickled_ind'
model_obj.load_data(path_to_normals, num_files=num_norms,
                    rhythm_type='normal')
model_obj.load_data(path_to_afibs, num_files=num_afibs,
                    rhythm_type='afib')

model_obj.get_100x_autoencoder()
    
#Run
model_obj.run_autoencoder(n_epochs=num_epochs)


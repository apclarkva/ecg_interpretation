from ml_models import Models
import numpy as np
import os
import pdb
os.environ['KMP_DUPLICATE_LIB_OK']='True'


def main():
    path_to_signals = '/data/ecg/normal_pickled_ind'
    model_obj = Models(path_to_signals, t_span=2048)

    model_obj.get_autoencoder()
    model_obj.current_model.summary()

    pdb.set_trace() 

    autoencoder = model_obj.current_model
    model_obj.load_from_npy(path_to_signals)
    autoencoder.fit(model_obj.input_data, model_obj.input_data, verbose=1, batch_size=300, epochs=40)



if __name__ == '__main__':
    main()

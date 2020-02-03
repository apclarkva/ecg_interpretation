from ml_models import Models
import unittest
import matplotlib.pyplot as plt
import numpy as np
import pdb
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

class TestModels(unittest.TestCase):
    """
    Test the Models class
    """
    def test_autoencoder(self):
        path_to_signals = './data/forAlex/normal_pickled'

        model_obj = Models(path_to_signals, t_span=2048)
        model_obj.load_from_npy(path_to_signals)
        model_obj.get_autoencoder()
        model_obj.current_model.summary()
        import pdb
        pdb.set_trace()
        
        #model_obj.input_data = np.concatenate((arr_1, arr_2, arr_3, arr_4, arr_5, arr_6), axis=0)[:, 0:1024, 0:2]
        #model_obj.input_data = np.concatenate((arr_1, arr_2), axis=0)[:, 0:1024, 0:12]

        index = 0
        for row in range(0,2400):
            min_zero = model_obj.input_data[index,:,0].min()
            min_one = model_obj.input_data[index,:,1].min()
            if min_zero < 0:
                model_obj.input_data[index,:,0] -= min_zero
            if min_one <0:
                model_obj.input_data[index,:,1] -= min_one 

            model_obj.input_data[index,:,0] /= model_obj.input_data[index,:,0].max()
            model_obj.input_data[index,:,1] /= model_obj.input_data[index,:,1].max()
            index += 1 



        autoencoder = model_obj.current_model
        autoencoder.fit(model_obj.input_data, model_obj.input_data, verbose=1, batch_size=300, epochs=8)
        pdb.set_trace()


if __name__ == '__main__':
    unittest.main()


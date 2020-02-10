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
    @classmethod
    def setUpClass(cls):
        num_norms = 10
        num_afibs = 10
        cls.model_obj = Models()
        
        path_to_afibs = 'data/ecg/afib_pickled_ind'
        path_to_normals = 'data/ecg/normal_pickled_ind'
        cls.model_obj.load_data(path_to_normals, num_files=num_norms,
                            rhythm_type='normal')
        cls.model_obj.load_data(path_to_afibs, num_files=num_afibs,
                            rhythm_type='afib')

    def test_input_init(self):
        afib_data_shape = self.model_obj.afib_data.shape
        training_data_shape = self.model_obj.normal_training.shape
        input_shape = self.model_obj.input_shape.get_shape()
        
        input_shape.assert_is_compatible_with(afib_data_shape)
        input_shape.assert_is_compatible_with(training_data_shape)

    def test_multi_class_output(self):
        """
        Assert: number of observations equals input
        Assert: number of classes equals pre-defined number
        """
        pass

    def test_binary_class_output(self):
        """
        Assert: number of observations equals input
        """
        pass
    
    def test_get_encoder(self):
        """
        Assert: self.encoder equals first half of model
        """



if __name__ == '__main__':
    unittest.main()

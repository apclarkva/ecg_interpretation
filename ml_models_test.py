from ml_models import Models
import unittest
import matplotlib.pyplot as plt
import pdb

class TestModels(unittest.TestCase):
    """
    Test the Models class
    """
    def test_autoencoder(self):
        path_to_signal = './data/forAlex/normal'

        model_obj = Models(path_to_signal, t_span=4096)
        model_obj.format_input_data()

        model_obj.get_autoencoder()
        model_obj.current_model.summary()

        autoencoder = model_obj.current_model
        autoencoder.fit(model_obj.input_data, model_obj.input_data, verbose=1, batch_size=10, epochs=3000)
        pdb.set_trace()


if __name__ == '__main__':
    unittest.main()


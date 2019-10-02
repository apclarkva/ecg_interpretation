import unittest
import deidentify_ecg
from xml_to_ECG import ECGSignal
import os
import shutil
import pdb


class TestDeidentifyECG(unittest.TestCase):
    """
    I want to test the methods required to deidentify XML data
    """
    def tearDown(self):
        """
        Run after each test in the method
        """
        try:
            expected_path_to_deidentified = './data/wcm_ecg_test_deidentified'
            shutil.rmtree(expected_path_to_deidentified)
        except FileNotFoundError:
            print('nothing to teardown')

    def test_deidentify_ecg_key_exists(self):
        path_to_data = './data/wcm_ecg_test'
        expected_path_to_deidentified = './data/wcm_ecg_test_deidentified'

        deidentify_ecg.deidentify(path_to_data)

        self.assertTrue(os.path.exists(expected_path_to_deidentified),
                        'the deidentify function did not create the correct \
            new directory')
        self.assertTrue(os.path.isfile(
            f'{expected_path_to_deidentified}/key.csv'),
            'the deidentify() function doesn\'t create a key')

    def test_deidentify_ecg_key_contains_info(self):
        path_to_data = './data/wcm_ecg_test'
        expected_path_to_deidentified = './data/wcm_ecg_test_deidentified'

        deidentify_ecg.deidentify(path_to_data)


#    def test_ecg_deidentify_no_demo_data(self):
#        pass
#
#
#    def test_ecg_deidentify_same_patient_key(self):
#        pass




if __name__ == '__main__':
    unittest.main()

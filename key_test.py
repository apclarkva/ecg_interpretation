import unittest
import deidentify_ecg
import os
import shutil
from key import Key
import pandas as pd
import pdb


class TestKey(unittest.TestCase):
    """
    I want to test the methods required to deidentify XML data
    """
    path_to_data = './data/test_files'
    expected_path_to_deidentified = './data/test_files_deidentified'
    example_patient = {
            'PatientID': '0000000',
            'DateofBirth': '01-21-1982',
            'PatientLastName': 'Sirieix',
            'PatientFirstName': 'Fred',
            'AcquisitionDate': '08-02-2019'
            }

    def tearDown(self):
        """
        Run after each test in the method
        """
        try:
            shutil.rmtree(self.expected_path_to_deidentified)
        except FileNotFoundError:
            print('nothing to teardown')

    def test_deidentify_ecg_key_exists(self):
        key = Key(self.path_to_data)
        key.write_key_to_file()
        
        self.assertTrue(os.path.exists(self.expected_path_to_deidentified),
                        'the deidentify function did not create the correct \
            new directory')
        self.assertTrue(os.path.isfile(
            f'{self.expected_path_to_deidentified}/key.csv'),
            'the deidentify() function doesn\'t create a key')

    def test_deidentify_ecg_saves_key(self):
        key = Key(self.path_to_data)
        key.deidentify_all_ecgs()
        key.write_key_to_file()

        new_key_df = pd.read_csv(
            f'{self.expected_path_to_deidentified}/key.csv')

        self.assertTrue(self.example_patient['PatientFirstName'] in
                        new_key_df['FIRST_NAME'].unique(),
                        'at least one patient was not correctly saved')
        self.assertTrue((key.key_df['ACQUISITION_DATE'] == new_key_df[
                'ACQUISITION_DATE']).all(), 
                'the saved CSV and current DataFrame are different')
        self.assertTrue((len(new_key_df.loc[new_key_df['FIRST_NAME'] == 'Fred']
                             ['DE_ID'].unique()) == 1) and
                        (len(new_key_df.loc[new_key_df['FIRST_NAME'] == 'Fred']
                             ['ACQUISITION_DATE'].unique()) > 1),
                        'the function creates a new id for existing patient')


if __name__ == '__main__':
    unittest.main()

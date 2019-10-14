import unittest
from process_uk_afib import ProcessUK
import os
import shutil
import pandas as pd
import pdb


class TestKey(unittest.TestCase):
    path_to_data = './data/forAlex'
    
    def test_deidentify_ecg_key_exists(self):
        uk_data = ProcessUK(self.path_to_data)
        uk_data.write_ecgs_key_and_csv()


if __name__ == '__main__':
    unittest.main()


import unittest
import os
from xml_to_ECG import ECGSignal
import pdb


class TestXMLtoECG(unittest.TestCase):
    def tearDown(self):
        try:
            path_deidentified = './data/ecg_biobank_test_deid.xml'
            os.remove(path_deidentified)
        except:
            print('nothing to teardown')

    def test_remove_fields_write(self):
        path = './data/ecg_biobank_test.xml'
        path_deidentified = './data/ecg_biobank_test_deid.xml'
        identifying_nodes = ['PatientInfo', 'PatientVisit']

        ecg_signal = ECGSignal(path)
        ecg_signal.remove_elements(identifying_nodes)
        ecg_signal.write_xml(path_deidentified)
        ecg_signal_deid = ECGSignal(path_deidentified)

        self.assertTrue(os.path.exists(path_deidentified),
                        'the .write_xml() method did not create a new file')
        self.assertTrue(not ecg_signal_deid.find_all_nodes(identifying_nodes[0]),
                        'the deidentified file has identiable information')

if __name__ == '__main__':
    unittest.main()

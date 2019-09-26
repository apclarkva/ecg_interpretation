import os
from xml_to_ECG import ECGSignal
import pdb


def deidentify(path):
    deidentified_directory = f'{path}_deidentified'
    ecg_file_names = os.listdir(path)
    identifiable_elements = [
        'PatientDemographics', 'TestDemographics', 'Order']

    create_folder_key(path, deidentified_directory)

    for ecg_file_name in ecg_file_names:
        current_signal = ECGSignal(f'{path}/{ecg_file_name}')
        current_signal.remove_elements(identifiable_elements)
        current_signal.write_xml(
            f'{deidentified_directory}/deid_{ecg_file_name}')


def create_folder_key(path, deidentified_directory):
    deidentified_directory= f'{path}_deidentified'
    deidentified_key = f'{deidentified_directory}/key.csv'

    if not os.path.exists(deidentified_directory):
        os.mkdir(deidentified_directory)

    if not os.path.exists(deidentified_key):
        f = open(deidentified_key, 'w')

    f.close()


if __name__ == '__main__':
    path = 'data/wcm_ecg_test' 
    deidentify(path)

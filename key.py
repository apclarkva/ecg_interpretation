import os
from xml_to_ECG import ECGSignal
import pdb
import pandas as pd


class Key:
    def __init__(self, directory_path,
                 identifiable_elements=['PatientDemographics',
                                        'TestDemographics', 'Order'],
                 nodes_for_key=['PatientID', 'PatientLastName',
                                'PatientFirstName', 'DateofBirth',
                                'Gender', 'AcquisitionDate']):
        self.identifiable_elements = identifiable_elements
        self.nodes_for_key = nodes_for_key
        self.path_to_raw_xml = directory_path
        self.path_to_deid_xml = f'{directory_path}_deidentified'
        self.key_df = pd.DataFrame(
            columns=['PROJECT_PT_ID',
                     'PATIENT_ID',
                     'LAST_NAME',
                     'FIRST_NAME',
                     'DOB',
                     'GENDER',
                     'ACQUISITION_DATE'])
        self.ecg_file_names = []

        
    def deidentify_all_ecgs(self):
        self.ecg_file_names = os.listdir(self.path_to_raw_xml)

        for ecg_file_name in self.ecg_file_names:
            current_signal = ECGSignal(
                f'{self.path_to_raw_xml}/{ecg_file_name}')
            self._write_current_signal_to_key(current_signal)

    def write_key_to_file(self):
        key_path = f'{self.path_to_deid_xml}/key.csv'
        if not os.path.exists(self.path_to_deid_xml):
            os.mkdir(self.path_to_deid_xml)

        if not os.path.exists(key_path):
            self.key_df.to_csv(key_path, index=False)

    def _write_current_signal_to_key(self, current_signal):
        patient_vals = []

        for tag_name in self.nodes_for_key:
            patient_vals.append(
                current_signal.find_all_nodes(tag_name)[0].text)

        patient_dict = self.get_patient_with_id(patient_vals)
        self.key_df = self.key_df.append(patient_dict, ignore_index=True)

    def get_patient_with_id(self, patient_values):
        df = self.key_df
        pt_id =  df[(df['PATIENT_ID'] == patient_values[0]) & 
                    (df['LAST_NAME'] == patient_values[1]) & 
                    (df['FIRST_NAME'] == patient_values[2]) &
                    (df['DOB'] == patient_values[3]) & 
                    (df['GENDER'] == patient_values[4])
                    ]['PROJECT_PT_ID']

        if len(df) == 0:
            pt_id = [0]
        elif len(pt_id) == 0:
            pt_id = [df['PROJECT_PT_ID'].max() + 1]
        else:
            pt_id = [pt_id.values[0]]

        patient_keys = df.columns
        patient_vals = pt_id + patient_values

        patient_dict = dict(zip(patient_keys, patient_vals))

        return patient_dict




#def deidentify(path):
#    deidentified_directory = f'{path}_deidentified'
#    ecg_file_names = os.listdir(path)
#    identifiable_elements = 
#    create_folder_key(path, deidentified_directory)
#
#    for ecg_file_name in ecg_file_names:
#        current_signal = ECGSignal(f'{path}/{ecg_file_name}')
#        current_signal.remove_elements(identifiable_elements)
#        current_signal.write_xml(
#            f'{deidentified_directory}/deid_{ecg_file_name}')
#
#
#def create_folder_key(path, deidentified_directory):
#    deidentified_directory= f'{path}_deidentified'
#    deidentified_key = f'{deidentified_directory}/key.csv'
#
#    if not os.path.exists(deidentified_directory):
#        os.mkdir(deidentified_directory)
#
#    if not os.path.exists(deidentified_key):
#        f = open(deidentified_key, 'w')
#
#    f.close()
#
#
#if __name__ == '__main__':
#    path = 'data/wcm_ecg_test'
#    deidentify(path)

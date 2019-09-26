import os
from xml_to_ECG import ECGSignal
import pdb
import pandas as pd


class Key:
    """
    This class is used to deidentify XML ECG files and create a key for
    reidentifying
    """
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
            columns=['DE_ID',
                     'PATIENT_ID',
                     'LAST_NAME',
                     'FIRST_NAME',
                     'DOB',
                     'GENDER',
                     'ACQUISITION_DATE'])
        self.ecg_file_names = []

    def deidentify_all_ecgs(self):
        """
        Loop through all the raw xml files in a folder and save
        identifying information to a key, with an auto-generated pt ID. 
        Insert the identifying ID into the XML file, then
        removes identifying information from the patient and writes it to
        an XML file.
        """
        if not os.path.isdir(self.path_to_deid_xml):
            if os.path.exists(self.path_to_deid_xml):
                os.remove(self.path_to_deid_xml)
            os.mkdir(self.path_to_deid_xml)

        self.ecg_file_names = os.listdir(self.path_to_raw_xml)

        for ecg_file_name in self.ecg_file_names:
            current_signal = ECGSignal(
                f'{self.path_to_raw_xml}/{ecg_file_name}')
            self._write_current_signal_to_key(current_signal)
            de_identifying_number = self.key_df.shape[0]
            current_signal.add_element('DeidentifyingNumber',
                    f'{de_identifying_number}', current_signal.ecg_root)
            current_signal.remove_elements(self.identifiable_elements)
            current_signal.write_xml(
                f'{self.path_to_deid_xml}/{de_identifying_number}.xml')

    def write_key_to_file(self):
        key_path = f'{self.path_to_deid_xml}/key.csv'
        if not os.path.isdir(self.path_to_deid_xml):
            if os.path.exists(self.path_to_deid_xml):
                os.remove(self.path_to_deid_xml)
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
                    ]['DE_ID']

        if len(df) == 0:
            pt_id = [0]
        elif len(pt_id) == 0:
            pt_id = [df['DE_ID'].max() + 1]
        else:
            pt_id = [pt_id.values[0]]

        patient_keys = df.columns
        patient_vals = pt_id + patient_values

        patient_dict = dict(zip(patient_keys, patient_vals))

        return patient_dict

if __name__ == '__main__':
    path = 'data/PATH_TO_FILES'
    key_obj = Key(path)
    key_obj.deidentify_all_ecgs()
    key_obj.write_key_to_file()

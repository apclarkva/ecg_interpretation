import os
from xml_to_ECG import ECGSignal
import pandas as pd


class Key:
    """
    This class is used to deidentify XML ECG files and create a key for
    reidentifying them
    """
    def __init__(self, directory_path,
                 identifiable_elements=['PatientDemographics',
                                        'TestDemographics', 'Order'],
                 nodes_for_key=['PatientID', 'PatientLastName',
                                'PatientFirstName', 'DateofBirth',
                                'Gender', 'AcquisitionDate'],
                 afib_key=None):
        """
        This initializes a Key object

        Parameters
        ----------
        deirectory_path: String
            The path to a directory of XML files you want to deidentify
        identifiable_elements: List of Strings
            A list of tag names that include identifiable information
        nodes_for_key: List of Strings
            A list of tag names that include identifiable information you want 
            to save to the key
        """
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


    def write_ecgs_key_and_csv(self):
        """
        Read in every xml file and save the strip data to a .csv file in either
        the normal folder or the ecg folder.
        Save identifying information to the key.
        """
        pt_keys_paths = self.get_paths_and_afib_ids(self.path_to_raw_xml)

        for pt in pt_keys_paths:
            new_pt = xml_to_ECG(pt[1])
            import pdb
            pdb.set_trace()
            



    def get_paths_and_afib_ids(self, path_to_data):
        """
        Finds all XML files in root, then returns them with an ID.
        
        Parameters
        ----------
        path_to_data: String
            Inside of this folder, there should be XML files. The files
            can be nested within other folders.

        Returns 
        -------
        file_paths: List of Lists
            A list of lists that contain the afib key identifier in postiion 1
            and the path to the file in position 2.
        """
        file_paths = []
        for root, dirs, files in os.walk(path_to_data):
            for file_name in files:
                if ('.xml' in file_name):
                    path = f'{root}/{file_name}'
                    key_id = file_name.split('_')[0]
                    file_paths.append([key_id, path])

        return file_paths

    def deidentify_all_ecgs(self):
        """
        TODO: CONSIDER DELETING THIS – DEPRECATED FROM 
        write_ecgs_key_and_csv()
        This method does two things:
            1. Loop through all the raw xml files in a folder and save
            identifying information to a key, with an auto-generated pt ID.
            2.Insert the identifying ID into the XML file, then remove
            identifying information from the patient and write it to an XML
            file.
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
        """
        This method writes the current key parameter to a .csv file called 
        key.csv.
        """
        key_path = f'{self.path_to_deid_xml}/key.csv'
        if not os.path.isdir(self.path_to_deid_xml):
            if os.path.exists(self.path_to_deid_xml):
                os.remove(self.path_to_deid_xml)
            os.mkdir(self.path_to_deid_xml)

        if not os.path.exists(key_path):
            self.key_df.to_csv(key_path, index=False)

    def _write_current_signal_to_key(self, current_signal):
        """
        This method should not be used outside of this class. It is used to 
        write the identifying information from a patient to the key parameter.

        Parameters
        ----------
        current_signal: ECGSignal Object
            This object includes information for the current patient    
        """
        patient_vals = []

        for tag_name in self.nodes_for_key:
            patient_vals.append(
                current_signal.find_all_nodes(tag_name)[0].text)

        patient_dict = self.get_patient_with_id(patient_vals)
        self.key_df = self.key_df.append(patient_dict, ignore_index=True)

    def get_patient_with_id(self, patient_values):
        """
        Determines an identification number for the patient, described by
        the identifying information in patient_values. If the patient exists
        in the key, then this function will find the original patient ID value.
        Otherwise, it will return a new ID, by incrementing the previous max ID

        Parameters
        ----------
        patient_values: List of Strings
            This contains identifying information from a current patient

        Returns
        -------
        patient_dict: Dictionary of patient information with ID 
            The dictionary contains key names that match the column names
            from the key parameter, including an ID key, which is added in
            this function.
        """
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
    PATH = 'data/PATH_TO_FILES'
    KEY_OBJ = Key(path)
    KEY_OBJ.deidentify_all_ecgs()
    KEY_OBJ.write_key_to_file()

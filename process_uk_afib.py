from xml_to_ECG import ECGSignal

import numpy as np
import pandas as pd
import os


class ProcessUK:
    """
    This class is used to deidentify XML ECG files and create a key for
    reidentifying them
    """

    def __init__(self, directory_path,
                 afib_key='afibKey'):
        """
        This initializes an object for processing UKbiobank data

        Parameters
        ----------
        directory_path: String
            The path to a directory of XML files you want to deidentify
        afib_key: String
            The name of the afib key – this should be located in the root of
            directory_path
        """
        self.path_to_raw_xml = directory_path
        self.afib_key = pd.read_csv(f'{directory_path}/{afib_key}',
                                    sep=' ',
                                    header=None)

    def write_ecgs_to_npy(self):
        """
        Read in every xml file and save the strip data to a .csv file in either
        the normal folder or the ecg folder.
        Save identifying information to the key.
        """
        pt_keys_paths = self.get_paths_and_afib_ids(self.path_to_raw_xml)

        index = 0
        for pt in pt_keys_paths:
            new_pt = ECGSignal(pt[1])
            diagnosis_nodes = new_pt.find_all_nodes('DiagnosisText')
            diagnoses = [element.text for element in diagnosis_nodes]
            try:
                is_normal = self.get_is_normal(pt[0], diagnoses)
                is_afib = self.get_is_afib(pt[0], diagnoses)
            except:
                is_normal = False
                is_afib = False
                

		
            if is_normal:
                classification = 'normal'
            elif is_afib:
                classification = 'afib'
            else:
                continue
            print(index)
            index += 1

            np.save(f'./{self.path_to_raw_xml}/{classification}_pickled_ind/{pt[0]}', 
                    new_pt.waveforms.values)


    def get_is_normal(self, pt_id, diagnoses):
        d_1 = diagnoses[0].lower()
        d_2 = diagnoses[1].lower()
        if ((d_1 == 'normal sinus rhythm') and (d_2 == 'normal ecg')) or \
                ((d_1 == 'sinus bradycardia') and (d_2 == 'otherwise normal ecg')):
            return 1

        return 0

    def get_is_afib(self, pt_id, diagnoses):
        """
        Returns 1 if the patient with id pt_id has afib and 0 if they are 
        normal

        Parameters
        ----------
        pt_id: String
            A string that is the patient identifier in the afib_key

        Returns
        -------
        is_afib: Boolean
            Returns true if the patient iwth pt_id has afib
        """
        for diagnosis in diagnoses:
            if ('fibrillation' in diagnosis.lower()):
                return 1
            return 0

        return 
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

if __name__ == '__main__':
    path_to_data = './data/ecg'
    UK_OBJ = ProcessUK(path_to_data)
    UK_OBJ.write_ecgs_to_npy()

    

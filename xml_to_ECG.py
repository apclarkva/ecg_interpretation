import xml.etree.ElementTree as et
import matplotlib.pyplot as plt
import numpy as np
import random
import pdb


class ECGSignal:
    """A class for reading in data from XML files, and displaying important
    information
    """
    def __init__(self, ecg_file):
        self.ecg_tree = et.parse(ecg_file)
        self.ecg_root = self.ecg_tree.getroot()
        self._waveforms = []
        self._arr_data = []

    @property
    def waveforms(self):
        """
        Return waveforms -- if they're not defined, then define them
        """
        if not self._waveforms:
            self._waveforms = self.find_all_nodes(self.ecg_root,
                                                  'WaveformData')
        return self._waveforms

    @property
    def arr_data(self):
        """
        Return arrhythmia data
        """
        if not self._arr_data:
            self._arr_data = self.find_all_nodes(self.ecg_root,
                                                 'ArrhythmiaData')
        return self._arr_data

    def print_all_tags(self, elem, level=0):
        """
        Print all tags, with nesting
        """
        tag = elem.tag
        print('    '*level+tag)
        for child in elem.getchildren():
            self.print_all_tags(child, level+1)

    def find_all_nodes(self, current_node, tag_name):
        """
        Finds and returns all the nodes for the given tag name
        """
        nodes = []

        if current_node.tag == tag_name:
            return [current_node]

        for child in current_node:
            nodes += self.find_all_nodes(child, tag_name)

        return nodes

    def plot_random_waveform(self):
        """
        Randomly select waveforms and plot them
        """
        num_waves = len(self.waveforms)
        random_wave = self.waveforms[int(random.uniform(0, 1)*num_waves)]

        data_as_str = random_wave.text.split(',')
        data = [int(numeric_string) for numeric_string in data_as_str]
        time = np.arange(0, len(data))*2/1000
        lead_number = random_wave.attrib['lead']

        plt.plot(time, data)
        plt.title(f'Lead Number {lead_number}')
        plt.xlabel('Time (s)')
        plt.ylabel('Voltage')
 
        plt.show(data)
 
    def plot_random_arrhythmia(self):
        strip_data = self.find_all_nodes(self.arr_data[0], 'Strip')
        num_strips = len(strip_data)
        random_strip = strip_data[int(random.uniform(0, 1)*num_strips)]

        waves = random_strip.getchildren()[1:]
        fig, axs = plt.subplots(3, 1)
        row = 0
        for wave in waves:
            data = wave.text.split(',')
            data = [int(numeric_string) for numeric_string in data]
            time = np.arange(0, len(data))*2/1000
            lead_number = wave.attrib['lead']
            axs[row].set_title(f'Lead {lead_number}')
            axs[row].plot(time, data)
            row = row + 1

        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    ECG_SIGNAL = ECGSignal('./data/ecg_biobank_test.xml')
    ECG_SIGNAL.print_all_tags(ECG_SIGNAL.ecg_root)
    ECG_SIGNAL.plot_random_arrhythmia()

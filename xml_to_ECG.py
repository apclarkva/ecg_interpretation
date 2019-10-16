import xml.etree.ElementTree as et
#import matplotlib.pyplot as plt
import numpy as np
import random
import pandas as pd
import pdb


class ECGSignal:
    """A class for reading in data from XML files, and displaying important
    information
    """
    def __init__(self, ecg_file=None, waveform_csv=None):
        if ecg_file:
            self.ecg_tree = et.parse(ecg_file)
            self.ecg_root = self.ecg_tree.getroot()

        if not waveform_csv:
            self._waveforms = pd.DataFrame()
        else:
            self._waveforms = pd.read_csv(waveform_csv)

        self._arr_data = []

    @property
    def waveforms(self):
        """
        Return waveforms -- if they're not defined, then define them
        """
        if self._waveforms.empty:
            self._waveforms = self.find_strip_data(
                'WaveformData')
        return self._waveforms

    @property
    def arr_data(self):
        """
        Return arrhythmia data
        """
        if not self._arr_data:
            self._arr_data = self.find_all_nodes('ArrhythmiaData',
                                                 self.ecg_root)
        return self._arr_data

    def print_all_tags(self, elem, level=0):
        """
        Print all tags, with nesting
        """
        tag = elem.tag
        print('    '*level+tag)
        for child in elem.getchildren():
            self.print_all_tags(child, level+1)

    def find_all_nodes(self, tag_name, current_node=None):
        """
        Finds and returns all the nodes for the given tag name
        """
        if current_node is None:
            current_node = self.ecg_root

        nodes = []

        if current_node.tag == tag_name:
            return [current_node]

        for child in current_node:
            nodes += self.find_all_nodes(tag_name, child)

        return nodes
 
    def find_strip_data(self, wf_tag_name='WaveformData',
                        strip_tag_name='StripData'):
        """
            Finds all waveform nodes that are inside StripData element.
        """
        strip_node = self.find_all_nodes(strip_tag_name, self.ecg_root)[0]
        waveforms = self.find_all_nodes(wf_tag_name, strip_node)

        waveform_pd = pd.DataFrame()

        for wave in waveforms:
            lead_name = wave.attrib['lead']
            lead_values = np.array([int(num_str) for num_str in
                                    wave.text.split(',')])
            waveform_pd[lead_name] = lead_values

        return waveform_pd

    def remove_elements(self, node_names):
        """
        Remove all nodes with node_names
        Args:
            node_names as a List
        """
        for node_name in node_names:
            nodes = self.find_all_nodes(node_name)
            for element in nodes:
                self.ecg_root.remove(element)

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

    def plot_random_arrhythmia(self, is_saved = False):
        strip_data = self.find_all_nodes('Strip', self.arr_data[0])
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
        plt.xlabel('Time (s)')
        plt.savefig('ECG_example_trace.png')
        plt.show()

    def plot_twelve_lead(self, is_saved=False):
        """
        Plot an image with all twelve leads
        """
        self.waveforms.plot(subplots=True,
                            layout=(6, 2),
                            figsize=(6, 6),
                            sharex=False,
                            sharey=False,
                            legend=False,
                            style=['k' for i in range(12)])
        axes = plt.gcf().get_axes()
        for ax in axes:
            ax.axis('off')
            
        plt.show()


        
    


    def write_xml(self, path):
        """
        Write the current tree to the given file path
        """
        self.ecg_tree.write(path)

    def add_element(self, element_name, element_text, first_child_of):
        if first_child_of is None:
            first_child_of = self.ecg_root

        new_element = et.Element(element_name)
        new_element.text = element_text

        first_child_of.insert(0, new_element)


if __name__ == '__main__':
    ECG_SIGNAL = ECGSignal(waveform_csv='./data/afib_example/4642804.csv')
    ECG_SIGNAL.plot_twelve_lead()

    #rand_wf = ECG_SIGNAL.waveforms[9].text
    #y = [c for c in rand_wf if c.isdigit()]
    # Can plot y

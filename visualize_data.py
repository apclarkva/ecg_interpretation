import xml.etree.ElementTree as et
import matplotlib.pyplot as plt
import numpy as np
import pdb

xtree = et.parse('./data/ecg_biobank_test.xml')
xroot = xtree.getroot()

for child in xroot:
    print(child.tag, child.attrib)
    try:
        for grandchild in child:
            print(f'    {grandchild.tag}')
            try:
                for great_grandchild in grandchild:
                    print(f'          {great_grandchild}')
            except:
                pass
    except:
        pass


all_name_elements = xtree.findall('*/Time')
print(all_name_elements)



def find_all_nodes(current_node, tag_name):
    nodes = []
    if current_node.tag == tag_name:
        return [current_node]
    else:
        for child in current_node:
            nodes += find_all_nodes(child, tag_name)
            

    return nodes


time_nodes = find_all_nodes(xroot, 'Time')
waveform_nodes = find_all_nodes(xroot, 'WaveformData')
full_disclosure_node = find_all_nodes(xroot, 'FullDisclosureData')

waveform_of_interest = 71 
data_as_str = waveform_nodes[0].text.split(',')
data = [int(numeric_string) for numeric_string in data_as_str] 
all_data_as_str = np.array(full_disclosure_node[0].text.split(','))
remove_t = np.char.find(all_data_as_str, '\t') != 0
all_data_as_str = all_data_as_str[remove_t]
remove_n = np.char.find(all_data_as_str, '\n') != 0
all_data_as_str = all_data_as_str[remove_n]
all_data = [int(numeric_string) for numeric_string in all_data_as_str] 

plt.plot(data)
plt.show()


def perf_func(elem, func, level=0):
    func(elem,level)
    for child in elem.getchildren():
        perf_func(child, func, level+1)

def print_level(elem,level):
    print ('    '*level+elem.tag)


perf_func(xroot, print_level)

if __name__ == '__main__':


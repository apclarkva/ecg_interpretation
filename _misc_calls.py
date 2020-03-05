from xml_to_ECG import ECGSignal

eg_ecg = ECGSignal(ecg_file='./data/eg_ecg_ace.xml')

full_waves = eg_ecg.find_strip_data(wf_tag_name='FullDisclosureData',strip_tag_name='FullDisclosure')
waves = eg_ecg.waveforms

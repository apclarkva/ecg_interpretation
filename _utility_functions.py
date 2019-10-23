from os import listdir
import numpy as np
from os import makedirs


def pickle_data(path_to_data, batch_size):

    file_names = listdir(path_to_data)
    num_observations = len(file_names)
    remainder = np.mod(num_observations, batch_size)

    file_ranges = np.arange(0, num_observations, batch_size)

    if remainder > 0:
        file_ranges = np.append(file_ranges, remainder)
    
    makedirs(f'{path_to_data}/pickled_{batch_size}')
    
    for start_val in file_ranges:
        if start_val == file_ranges[-1]:
            break
        
        index = 0
        num_observations = file_ranges[index + 1] - start_val

        batch_data = np.zeros((num_observations, 5000, 12))

        for file_name in file_names[start_val:(file_ranges[index + 1])]:
            current_path = f'{path_to_data}/{file_name}'
            current_data = np.loadtxt(current_path, skiprows=1, delimiter=',')

            batch_data[index, :, :] = current_data
            index += 1

        
        np.save(f'{path_to_data}/pickled_{batch_size}/pickled_{start_val}',
                batch_data)

def get_train_val_loss(file_out, write_file):
    with open(file_out, 'r') as fp:
        line = line = fp.readline()

        new_file = np.array([])
        while line:
            if 'val_loss' in line:
                new_file = np.append(new_file, line.strip())
            if 'Evaluation of' in line:
                new_file = np.append(new_file, line.strip())
                 

            print(line.strip())
            
            line = fp.readline()

        np.savetxt(write_file, new_file, fmt='%s')





if __name__ == '__main__':
    slurm = 'slurm-1116824'
    file_name = f'{slurm}.out'
    write_to = f'./data/auto_48x_4480obs_4s.csv'
    get_train_val_loss(file_name, write_to)



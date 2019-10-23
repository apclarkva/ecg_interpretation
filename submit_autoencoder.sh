#! /bin/bash -l
 
#SBATCH --partition=panda   # cluster-specific
#SBATCH --nodes=1
#SBATCH --ntasks=128
#SBATCH --job-name=autoencoder
#SBATCH --time=20:00:00   # HH/MM/SS
#SBATCH --mem=32G

source ~/.bashrc
spack load -r /cypfv4n miniconda3@4.3.14%gcc@6.3.0 arch=linux-centos7-x86_64

echo "Starting at:" `date` >> hello_slurm_output.txt
source activate /athena/christinilab/scratch/apc223/.conda/envs/ml-env

echo $SLURM_JOB_NODELIST

python3 main.py 

exit

#! /bin/bash -l
 
#SBATCH --partition=panda   # cluster-specific
#SBATCH --nodes=1
#SBATCH --ntasks=28
#SBATCH --job-name=autoencoder
#SBATCH --time=08:00:00   # HH/MM/SS
#SBATCH --mem=28G

source ~/.bashrc
spack load -r /cypfv4n miniconda3@4.3.14%gcc@6.3.0 arch=linux-centos7-x86_64
source activate ml-env

echo $SLURM_JOB_NODELIST

python3 main.py 

exit

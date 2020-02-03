#! /bin/bash -l

#SBATCH --partition=panda-gpu
#SBATCH --nodes=1
#SBATCH --ntasks=24
#SBATCH --job-name=autoencoder-200x
#SBATCH --time=48:00:00   # HH/MM/SS
#SBATCH --mem=24G
#SBATCH --gres=gpu

source ~/.bashrc
spack load -r /cypfv4n miniconda3@4.3.14%gcc@6.3.0 arch=linux-centos7-x86_64

echo "Starting at:" `date` >> hello_slurm_output.txt
source activate /athena/christinilab/scratch/apc223/.conda/envs/ml-envgpu

echo $SLURM_JOB_NODELIST

python3 main.py

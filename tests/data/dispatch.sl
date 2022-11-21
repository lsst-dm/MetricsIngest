#!/bin/bash -l
#SBATCH -p roma
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --mem=20G
#SBATCH -t 54:00:00
#SBATCH -J verify
#SBATCH --output=dispatch_w_2022_42.%j.log
#SBATCH --error=dispatch_w_2022_42.%j.log
srun dispatch.sh

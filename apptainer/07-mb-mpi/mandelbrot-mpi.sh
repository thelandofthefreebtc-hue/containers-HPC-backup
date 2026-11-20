#!/bin/bash

#SBATCH --job-name=mandelbrot-mpi
#SBATCH --ntasks=4
#SBATCH --nodes=2
#SBATCH --cpus-per-task=2
#SBATCH --output=mandelbrot-mpi.log

module load OpenMPI/5.0.3-GCC-13.3.0

export PMIX_MCA_psec=native
mpirun --n $SLURM_NTASKS apptainer exec mb-mpi.sif mandelbrot-mpi.py

# Containers on Supercomputers (Apptainer HPC Workshop)

Hands-on exercises, Apptainer definition files (`.def`), Slurm batch scripts, and cluster notes from the [SLING Containers on Supercomputers](https://doc.sling.si/workshops/containers-hpc/) workshop.

## Repository Structure

| Directory / File | Topic & Focus |
| :--- | :--- |
| `apptainer/01-uporabimo-vsebnik` | Pulling and running existing containers from registries |
| `apptainer/02-peskovnik` | Interactive container builds using writable sandboxes |
| `apptainer/03-recept` | Reproducible container builds from `.def` definition files |
| `apptainer/04-python-scilib` | Packaging Python and scientific libraries inside containers |
| `apptainer/05-mb-cpu` | Running CPU-bound workloads (Mandelbrot set) via Slurm |
| `apptainer/06-mb-gpu` | GPU-accelerated containerized workloads |
| `apptainer/07-mb-mpi` | Multi-node parallel execution with MPI and Slurm |
| `apptainer/08-x` | Graphical User Interfaces (X11 forwarding and remote output) |
| `apptainer/modrec` | Complete `.def` recipe reference (`fortune`) and host `--bind` mounting |
| `NOTES.md` | Practical HPC cluster fixes and workarounds |

## Quick Reference Commands

```bash
# Build a container without root privileges
apptainer build --fakeroot <image>.sif <recipe>.def

# Bind-mount a host directory into a container at runtime
apptainer run --bind ./host_dir:/container_dir <image>.sif

# Fix PMIx/Munge MPI warning on HPC clusters
export PMIX_MCA_psec=native

## Notes

Large binary artifacts (`.sif` container images, `.sb` sandboxes, Slurm `.out`/`.err` logs, and datasets) are excluded via `.gitignore` to keep the repository lightweight and reproducible.

## Reference

Based on the [SLING (Slovenian National Supercomputing Network)](https://doc.sling.si/workshops/containers-hpc/) workshop curriculum.

## Workshop Outputs

![Mandelbrot Set](apptainer/05-mb-cpu/mandelbrot.jpg)

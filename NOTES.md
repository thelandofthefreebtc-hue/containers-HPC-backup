# Apptainer HPC Workshop Notes

- **Fix PMIx/Munge MPI warning:** `export PMIX_MCA_psec=native`
- **Build without sudo:** `apptainer build --fakeroot <image>.sif <recipe>.def`
- **View images when login node lacks `xauth`:** Copy to local machine with `scp` or use VS Code Remote - SSH.
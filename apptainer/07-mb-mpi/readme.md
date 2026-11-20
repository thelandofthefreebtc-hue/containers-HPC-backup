# Vaja 7: Vsebnik za porazdeljeno računanje z MPI

## Kaj bomo naredili

Pripravili bomo vsebnik s knjižnico OpenMPI za porazdeljeno računanje. Izhajali bomo iz vsebnika, ki smo si pa pripravili v vaji 4. Izberemo enako verzijo knjižnice`OpenMPI`, kot je nameščena na gruči, in jo z ustreznimi stikali prevedemo. Dodatno namestimo še paket `mpi4py` z ovojnico za knjižnico MPI za python. V vsebnik skopiramo tudi program `mandelbrot-mpi.py` in konfiguracijsko datoteko `default.conf`.

Nazadnje na superračunalniškem sistemu preverimo, da nam vsebnik pravilno deluje.

Vajo lahko izvedemo, če predhodno zgradimo vsebnik iz vaje 4.

## Postopek

1. Pripravimo glavo recepta. 

    ```
    Bootstrap: localimage
    From: ../04-python-scilib/python-scilib.sif
    ```

2. V razdelku `%files` poskrbimo za prenos programa in konfiguracijske datoteke
    
    ```shell
    ./prg/mandelbrot-mpi.py /exec/
    ./prg/default.conf /exec/
    ```

3. V razdelku `%post` poleg osnovnih okoljskih spremenljivk (`LC_ALL` in `DEBIAN_FRONTEND`) nastavimo pot do programov in namestimo pakete, ki jih potrebujemo za prevajanje in namestitev OpenMPI.

    ```shell    
    export LC_ALL=C    
    export DEBIAN_FRONTEND=noninteractive

    chmod a+rx /exec/*.py
    chmod a+r /exec/*.conf

    apt update -y
    apt install -y wget
    apt install -y build-essential
	apt install -y openssh-client
    ```

4. Dodatno v razdelku `%post` prenesemo in namestimo še knjižnico [`OpenMPI`](https://www.open-mpi.org/) in komunikacijsko knjižnico ['UCX'](https://openucx.org/). 

    - Najprej prenesemo in prevedemo knjižnico UCX, ki jo za komunikacijo uporablja OpenMPI.

        ```shell
        export UCX_VER_MAIN=1.18
        export UCX_VER_SUB=1
        export UCX_VER=${UCX_VER_MAIN}.${UCX_VER_SUB}
        cd /opt
        wget https://github.com/openucx/ucx/releases/download/v${UCX_VER}/ucx-${UCX_VER}.tar.gz
        tar xvf ucx-${UCX_VER}.tar.gz
        cd ucx-${UCX_VER}
        ./configure --prefix=/opt/ucx-${UCX_VER} --enable-mt
        make -j 10
        make install
        ```

    - Pri namestitvi OpenMPI izberemo verzijo, ki je enaka kot na superračunalniški gruči. Za gruči Arnes je to trenutno `5.0.3`. Namestitev izvedemo v mapi `/opt`. Na koncu arhivsko datoteko `openmpi-5.0.3.tar.gz` pobrišemo. Knjižnico OpenMPI želimo povezati z razvrščevalnikom Slurm, zato dodamo stikali `--with-slurm` in `--with-pmix`.

        ```shell
        export MPI_VER_MAIN=5.0
        export MPI_VER_SUB=3
        export MPI_VER=${MPI_VER_MAIN}.${MPI_VER_SUB}
        cd /opt
        wget https://download.open-mpi.org/release/open-mpi/v${MPI_VER_MAIN}/openmpi-${MPI_VER}.tar.gz
        tar xvzf openmpi-${MPI_VER}.tar.gz
        rm -rf /opt/openmpi-${MPI_VER}.tar.gz
        mv openmpi-${MPI_VER} openmpi
        cd openmpi
        /configure --prefix=/opt/openmpi --with-slurm --with-pmix=internal --with-libevent --with-hwloc --with-ucx=/opt/ucx-${UCX_VER}
        make all install
        cd ..
        ```

5. V razdelku `%post` namestimo še paket `mpi4py`. Paket mora pri nameščanju poznati pot do izvršljivih datotek in knjižnic MPI, zato najprej ustrezno dopolnimo spremenljivki okolja `PATH` in `LD_LIBRARY_PATH`, nato pa ga namestimo z namestitvenim programom `pip3`.

    ```shell
    export LD_LIBRARY_PATH=/opt/openmpi/lib:${LD_LIBRARY_PATH}
    export PATH=/opt/openmpi/bin:${PATH}

	pip3 install mpi4py --break-system-packages
    ```

6. Ob namestitvi OpenMPI izvedemo ukaz `./configure`, ki med drugim nastavi tudi množico spremenljivk okolja. Te spremenljivke okolja morajo biti nastavljene tudi ob delu z vsebnikom. Zato jih vpišemo v razdelek `%environment`.

    ```shell
    # general
    export LC_ALL=C    
    export PATH=/exec:${PATH}

    # UCX
    export LD_LIBRARY_PATH=/opt/ucx-${UCX_VER}/lib:${LD_LIBRARY_PATH}
    export PATH=/opt/ucx-${UCX_VER}/bin:${PATH}

    # OpenMPI
    export LD_LIBRARY_PATH=/opt/openmpi/lib:${LD_LIBRARY_PATH}
    export PATH=/opt/openmpi/bin:${PATH}
    export OMPI_DIR=/opt/openmpi/build
    ```

7. Vsebnik po potrebi opremimo z zagonsko skripto, testno skripto in navodili za uporabo.

8. Zaženemo gradnjo vsebnika in si privoščimo dolgo kavo.

    ```console
    $ apptainer build --fakeroot mb-mpi.sif mb-mpi.def
    ```

9. Vsebnik še preizkusimo: 

   - Zaženemo ga na računalniku, ki smo ga uporabili za gradnjo:

        ```console
        $ apptainer exec mb-mpi.sif mpirun --n 4 mandelbrot-mpi.py
        ```

    - Zaženemo ga na superračunalniškem sistemu preko razvrščevalnika `mpirun` v vsebniku:
  
        ```console
        $ srun --ntasks=1 --nodes=1 --cpus-per-task=4 apptainer exec mb-mpi.sif mpirun --n 4 --oversubscribe mandelbrot-mpi.py
        ```

    - Zaženemo ga še na več računskih vozliščih, tako da `mpirun` zažene vsebnik.
    
        Pripravimo skripto `mandelbrot-mpi.sh` 

        ```console
        #!/bin/bash
        #SBATCH --job-name=mandelbrot-mpi
        #SBATCH --ntasks=4
        #SBATCH --nodes=2
        #SBATCH --cpus-per-task=2
        #SBATCH --output=mandelbrot-mpi.log
        
        module load OpenMPI
        mpirun -n $SLURM_NTASKS apptainer exec mb-mpi.sif mandelbrot-mpi.py
        ```
  
        in jo zaženemo

        ```console
        $ sbatch mandelbrot-mpi.sh
        ```

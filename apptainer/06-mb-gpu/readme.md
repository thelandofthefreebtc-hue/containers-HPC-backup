# Vaja 6: Vsebnik za grafične procesne enote

## Kaj bomo naredili

Pripravili bomo vsebnik s knjižnicami CUDA za računanje na grafičnih procesnih enotah. V repozitoriju [dockerhub](https://hub.docker.com/) Nvidia objavlja raznorazne vsebnike. Najdemo jih na povezavi [https://hub.docker.com/r/nvidia/cuda](https://hub.docker.com/r/nvidia/cuda). Izberemo vsebnik `12.8.1-devel-ubuntu24.04`, ki vključuje le najosnovnejše knjižnice. 

V vsebnik namestimo še potrebne programe. Tokrat namestimo ogrodje [Miniconda](https://docs.conda.io/en/latest/miniconda.html), v okviru katerega se nam namesti tudi python. Dodatno namestimo pakete `numpy`, `Pillow`, `numba` in `cuda-nvvm`. V vsebnik skopiramo še program `mandelbrot-gpu.py` in konfiguracijsko datoteko `default.conf`.

Nazadnje preverimo, da nam vsebnik pravilno deluje.

## Postopek

1. V glavo recepta vpišemo

    ```
    Bootstrap: docker
    From: nvidia/cuda:12.8.1-devel-ubuntu24.04
    ```

2. V razdelku `%files` poskrbimo za prenos programa in konfiguracijske datoteke.

    ```shell 
    ./prg/mandelbrot-gpu.py /exec/
    ./prg/default.conf /exec/
    ```

3. V razdelku `%post` nastavimo standardne spremenljivke okolja in s programom `apt` namestimo `wget`, ki ga potrebujemo za prenos ogrodja `Miniconda`. Prenešenim datotekam nastavimo potrebne pravice.

    ```shell 
    export LC_ALL=C    
    export DEBIAN_FRONTEND=noninteractive
    export CUDA_HOME=/usr/local/cuda

    apt update -y 
    apt install -y wget

    chmod a+rx /exec/*.py
    chmod a+r /exec/*.conf
    
    export PATH=/exec:${PATH}
    ```

4. Sledimo [navodilom](https://conda.io/projects/conda/en/latest/user-guide/install/index.html) za namestitev programskega paketa Miniconda. Ukazu `wget` s stikalom `-O` določimo ime prenešene datoteke. Pri klicu skripte za namestitev `Miniconda.sh` s stikalom `-b` (_angl. batch_) zahtevamo tiho namestitev, s stikalom `-p` pa določimo mapo, kamor naj se namestitev izvede. Po končani namestitvi pobrišemo namestitveno datoteko in v okoljsko spremenljivko `PATH` dodamo pot do nameščenih programov.

    ```shell
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O Miniconda.sh 
    /bin/bash Miniconda.sh -b -p /opt/conda
    rm Miniconda.sh
    export PATH=/opt/conda/bin:${PATH}
    ```

5. Namestimo še pakete za python.

    ```shell
    conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
    conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r
    conda install -y -c conda-forge -c nvidia \
        numpy \
        pillow \
        numba \
        cuda-nvvm \
        "cuda-version=12.8"
    
    conda clean -afy 
    ```

6. Vsebnik po potrebi opremimo z zagonsko skripto, testno skripto in navodili za uporabo.

7. Zgradimo vsebnik

    ```console
    $ apptainer build --fakeroot mb-gpu.sif mb-gpu.def
    ```

8. Program v vsebniku zaženemo na računskem vozlišču.

    ```console
    $ srun --ntasks=1 --partition=gpu --gpus=1 apptainer exec --nv mb-gpu.sif mandelbrot-gpu.py
    ```

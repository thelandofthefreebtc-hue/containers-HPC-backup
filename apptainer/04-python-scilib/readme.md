# Vaja 4: Vsebnik z jezikom python, nekaj paketi in potrebnimi knjižnicami

## Kaj bomo naredili?

Izhajali bomo iz vsebnika `ubuntu:latest`, gre za najnovejšo različico verzije LTS (_angl. Long Term Support_).

Vanj bomo s programom `apt` namestili:

- osnovna orodja za prevajanje, `build-essential`,
- knjižnico TBB za večnitenje, `libtbb-dev`,
- programski jezik python3, `python3-dev`,
- program `pip` za nameščanje paketov v python, `python3-pip`,

s programom `pip` pa še pakete: 

- `numpy`, 
- `Pillow`, 
- `tbb` in 
- `numba`.

## Postopek

Pripravimo recept `python-scilib.def`:

1. V glavi nastavimo

    ```
    Bootstrap: docker
    From: ubuntu:latest
    ```


2. V razdelek `%environment` vključimo standardno nastavitev lokalizacije.

    ```shell
    export LC_ALL=C    
    ```

3. V razdelek `%post` dodamo standardni nastavitvi okolja in izvedemo namestitve. Najprej s programom `apt`

    ```shell
    export LC_ALL=C    
    export DEBIAN_FRONTEND=noninteractive

    apt -y update
    apt -y install build-essential
    apt -y install libtbb-dev
    apt -y install python3-dev
    apt -y install python3-pip
    ```

    in nato še s programom `pip3`:

    ```
    pip3 install numpy --break-system-packages
    pip3 install Pillow --break-system-packages
    pip3 install tbb --break-system-packages
    pip3 install numba --break-system-packages
    ```
    
    Stikalo `--break-system-packages` moramo dodati, ker pakete nameščamo sistemsko.

4. V razdelku `%test` preverimo verzije nameščenih knjižnic

    ```
    python3 --version
    python3 -c "import numpy; print('numpy', numpy.__version__)"
    python3 -c "import PIL; print('PIL', PIL.__version__)"
    python3 -c "import numba; print('numba', numba.__version__)"
    ```

5. Dodamo še oznake vsebnika (`%labels`) in navodila za uporabo (`%help`)

6. Vsebnik zgradimo in preverimo testni izpis.

    ```console
    $ apptainer build --fakeroot python-scilib.sif python-scilib.def
    ```

7. Zgenerirajmo prvo sliko. Tokrat bomo zagnali program v pythonu, ki ga imamo v mapi `prg`.

    ```console
    $ srun --ntasks=1 apptainer exec python-scilib.sif python3 ./prg/mandelbrot-seq.py
    ```

    V nadaljevanju se bomo potrudili in ukaz skrajšali.

8. Sliko poglejmo z vsebnikom `firbec` iz vaje 3

    ```console
    $ ../03-recept/firbec.sif mandelbrot.jpg
    ```

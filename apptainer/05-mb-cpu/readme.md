# Vaja 5: Mandelbrotova množica na procesorskih jedrih

## Kaj bomo naredili?

Izhajali bomo iz vsebnika `python-scilib.sif`, ki smo ga zgradili v prejšnji nalogi.

Vanj bomo iz mape `./prg` skopirali programa `mandelbrot-seq.py`, `mandelbrot-par.py` in konfiguracijsko datoteko `default.conf`. Mapo `/exec` vključimo v spremenljivko `PATH`, v kateri so navedene mape, kjer operacijski sistem išče izvršljive datoteke. Vsem uporabnikom nastavimo še pravice za zaganjanje obeh programov in za branje konfiguracijske datoteke. Vsebnik opremimo z navodili za uporabo.

Vajo lahko izvedemo, če predhodno zgradimo vsebnik iz vaje 4.

## Postopek

1. Pripravimo glavo recepta. 

    ```
    Bootstrap: localimage
    From: ../04-python-scilib/python-scilib.sif
    ```

2. V razdeleku `%files` poskrbimo za prenos programov
    
    ```shell
    ./prg/mandelbrot-seq.py /exec/
    ./prg/mandelbrot-par.py /exec/
    ./prg/default.conf /exec/
    ```

3. V razdelku `%post` poleg osnovnih okoljskih spremenljivk (`LC_ALL` in `DEBIAN_FRONTEND`) nastavimo pot do programov in pravice.

    ```shell
    export LC_ALL=C    
    export DEBIAN_FRONTEND=noninteractive

    export PATH=/exec:${PATH}

    chmod a+rx /exec/*.py
    chmod a+r /exec/*.conf

4. Vsebnik po potrebi opremimo z zagonsko skripto, testno skripto in navodili za uporabo.

5. Zgradimo vsebnik

    ```console
    $ apptainer build --fakeroot mb-cpu.sif mb-cpu.def
    ```

6. Oba programa v vsebniku nekajkrat zaženemo na računskih vozliščih in opazujemo čase računanja. Vsakič zahtevamo štiri procesorska jedra. Zdaj nam pri klicu programa ni več potrebno navajati `python3` in poti do `programov`.

    ```console
    $ srun --ntasks=1 --cpus-per-task=4 apptainer exec mb-cpu.sif mandelbrot-seq.py
    $ srun --ntasks=1 --cpus-per-task=4 apptainer exec mb-cpu.sif mandelbrot-seq.py
    $ srun --ntasks=1 --cpus-per-task=4 apptainer exec mb-cpu.sif mandelbrot-par.py
    $ srun --ntasks=1 --cpus-per-task=4 apptainer exec mb-cpu.sif mandelbrot-par.py
    ```
Ob prvem zaganjanju programa `mandelbrot-par.py` knjižnica `numba` prevede funkcijo `mandelbrot_colors` in prevedeno kodo shrani v mapo `cd ~/.cache/numba`. Drugo zaganjanje programa je hitrejše, saj python uporabi že prevedeno kodo.
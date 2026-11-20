# Vaja 8: X

## Kaj bomo naredili?

[Sistem X Window](https://www.x.org/wiki/), X11, ali preprosto X, je sistem za prikazovanje računalniške grafike v porazdeljenem okolju. Z njim lahko pripravljamo uporabniške vmesnike, ki na oddaljenem računalniku prikazujejo bitno grafiko in omogočajo delo z vhodnimi napravami kot sta tipkovnica in miška.

Protokol X lahko izkoristimo za interaktivno delo s programom, ki je nameščen v vsebnik in ima grafični uporabniški vmesnik. Eden takih je program [`nomacs`](https://nomacs.org/) za prikazovanje in osnovno delo s slikami.

Izhajali bomo iz vsebnika `ubuntu:20.04` in vanj namestili programski paket `nomacs` in testno sliko.

## Postopek

1. V glavi nastavimo

    ```
    Bootstrap: docker
    From: ubuntu:24.04
    ```

2. V razdelku `%files` skopiramo sliko v mapo `/img`

    ```
    ./files/* /img/    
    ```

3. V razdelek `%environment` vključimo standardno nastavitev

    ```shell
    export LC_ALL=C    
    ```

4. V razdelek `%post` dodamo standardni nastavitvi in izvedemo namestitev s programom `apt` in pravice za branje slik v mapi `/img`.

    ```shell
    export LC_ALL=C    
    export DEBIAN_FRONTEND=noninteractive

    apt -y update
    apt -y install nomacs

    chmod a+r /img/*
    ```

5. Vsebnik po potrebi opremimo z zagonsko skripto, testno skripto in navodili za uporabo.

6. Zaženemo gradnjo vsebnika.

    ```console
    $ apptainer build --fakeroot x.sif x.def
    ```

7. Vsebnik še preizkusimo. Za preizkus potrebujemo odjemalca SSH, ki podpira protokol X. Na operacijskih sistemih Linux odjemalca zaženemo s stikalom `-X`

    ```console
    $ ssh -X slingXXX@nsc-login.ijs.si
    ```
    
    Na operacijskem sistemu macOS na enak način uporabimo stikalo `-Y`. Na operacijskem sistemu Windows si najprej namestimo ustreznega odjemalca. Protkol X med drugim podpirata [Putty](https://www.putty.org/) (omogočiti moramo možnost _X11 Forwarding_) in [Mobaxterm](https://mobaxterm.mobatek.net/).

    Zaženemo vsebnik in si ogledamo ustvarjene Mandelbrotove množice.

    ```console
    $ ./x.sif
    ```

    ali 

    ```console
    $ ./x.sif ../05-mb-cpu/mandelbrot.jpg
    ```

8.  V izpisu opazimo napako - program ne najde mape v vsebniku.

    ```
    QStandardPaths: XDG_RUNTIME_DIR points to non-existing path '/run/user/1977400034', please create it with 0700 permissions.
    [INFO] Hi there
    [INFO] theme loaded from "/usr/share/nomacs/Image Lounge/themes/Light-Theme.css"
    [INFO] CSS loaded from:  ":/nomacs/stylesheet.css"
    [INFO] local client created in:  6 ms
    [INFO] Initialization takes:  1 sec
    [INFO] "/img/210322_VEGA_083.jpg" loaded in 27 ms
    ```

    Z ukazom `mkdir temp` ustvarimo lokalno mapo `./temp/` in jo pri zagonu vsebnika povežemo z  mapo v vsebniku.

    ```console
    $ apptainer run --bind ./temp:/run/user/1977400034 x.sif
    ```

    Napake ni več.

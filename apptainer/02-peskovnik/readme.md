# Vaja 2: Zgradimo svoj vsebnik interaktivno

## Kaj bomo naredili?

Na delavnici bomo pripravljali vsebnike za generiranje slik. Da si bomo rezultate lahko hitro ogledali, si pripravimo vsebnik.

Tokrat bomo za osnovo vzeli vsebnik Ubuntu, ki ga bomo poiskali na repozitoriju [dockerhub](https://hub.docker.com/). V iskalno vrstico vpišemo **ubuntu** in izberemo vsebnik **ubuntu** iz nabora **Docker Official Images**. V veliko primerih je na repozitoriju Docker na voljo več različic vsebnikov, vsaka različica je označena s svojo značko (_angl. supported tags_). Z značkami lahko bolj natančno določimo, katero različico sistema želimo. Odločimo se za zadnjo verzijo vsebnika z značko `latest`. 

Za pregledovanje slik bomo uporabili programček `viu`, ki ga je pripravil Atanas Yankov. Najdemo ga na repozitoriju [GitHub](https://github.com/atanunq/viu). Na repozitoriju je poleg izvorne kode objavil tudi izvršljivo datoteko, ki jo bomo naložili v naš vsebnik. Povezava na izvršljivo datoteko: [https://github.com/atanunq/viu/releases/download/v1.4.0/viu](https://github.com/atanunq/viu/releases/download/v1.4.0/viu).

Za testiranje si bomo v vsebnik namestili še sliko superračunalnika Vega, ki jo najdemo na spletnih straneh [Izum](https://www.izum.si/hpc/). Povezava na sliko: [https://www.izum.si/wp-content/uploads/2021/03/210322_VEGA_083.jpg](https://www.izum.si/wp-content/uploads/2021/03/210322_VEGA_083.jpg).


## Postopek

1. Pripravimo si spremenljiv vsebnik (peskovnik), izhajali bomo iz operacijskega sistema `ubuntu:latest`. 

    ```console
    $ apptainer build --sandbox firbec.sb docker://ubuntu:latest
    ```

2. Vstopimo v vsebnik, pri tem pazimo, da imamo skrbniške pravice in dovoljenje za pisanje.

    ```console
    $ apptainer shell --fakeroot --writable firbec.sb
    ```

3. V vsebniku nam manjka program `wget`, s katerim lahko enostavno pretakamo vsebine s spleta. Da ga namestimo, najprej programu `apt` (_angl. Advanced Package Tool_) posodobimo povezave do repozitorijev, nato pa program namestimo v vsebnik

    ```console
    Apptainer> apt update -y
    Apptainer> apt install -y wget
    ```

4. Ustvarimo mapo `/exec` in programček `viu` s spleta prenesemo vanjo. Progamčku nastavimo potrebne pravice za dostop.

    ```console
    Apptainer> mkdir /exec
    Apptainer> wget -P /exec https://github.com/atanunq/viu/releases/download/v1.4.0/viu
    Apptainer> chmod a+rx /exec/viu
    ```

5. Ustvarimo mapo za slike `/img` in vanjo prenesimo sliko superračunalnika Vega.
    
    ```console
    Apptainer> mkdir /img
    Apptainer> wget -P /img https://www.izum.si/wp-content/uploads/2021/03/210322_VEGA_083.jpg
    Apptainer> chmod a+r /img/*
    ```

6. Poglejmo sliko

    ```console
    Apptainer> /exec/viu /img
    ```

7. Poskrbimo še, da ob zagonu vsebnika z ukazom `apptainer run` prikažemo slike v mapi, podani kot parameter, če parametra ni, pa prikažemo slike v mapi `/img`.

    ```console
    Apptainer> (echo '#!/bin/sh'; echo 'if [ $# -gt 0 ]; then /exec/viu $@; else /exec/viu /img; fi') > /singularity
    
    Apptainer> cat /singularity
    #!/bin/sh
    if [ $# -gt 0 ]; then /exec/viu $@; else /exec/viu /img; fi
    ```
8. Z ukazom `exit` zapustimo vsebnik.

9. Na gostitelja prenesemo še eno sliko in jo prikažimo.

    ```console
    $ wget https://www.izum.si/wp-content/uploads/2021/03/210326_VEGA_012-min.jpg    
    $ apptainer run firbec.sb .    
    ```
10. Nazadnje vsebnik pretvorimo v nespremenljivega in ga preverimo.
    
    ```console
    $ apptainer build --fakeroot firbec.sif firbec.sb
    $ ./firbec.sif
    ```

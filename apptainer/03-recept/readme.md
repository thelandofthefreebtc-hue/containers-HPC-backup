# Vaja 3: Zgradimo svoj vsebnik z receptom

## Kaj bomo naredili?

Za vsebnik iz vaje Vaje 2 pripravimo recept za gradnjo.

Spet bomo za osnovo uporabili vsebnik `ubuntu:latest` iz repozitorija [dockerhub](https://hub.docker.com/) in vanj namestili izvršljivo datoteko programa `viu` iz repozitorija [GitHub](https://github.com/atanunq/viu). Za testiranje bomo v vsebnik dodali še sliko superračunalnika Vega: [https://www.izum.si/wp-content/uploads/2021/03/210322_VEGA_083.jpg](https://www.izum.si/wp-content/uploads/2021/03/210322_VEGA_083.jpg).

Programček `viu` bomo predhodno prenesli v mapo `files`, sliko pa bomo v vsebnik naložili neposredno iz spleta. Za pretakanje s spleta si moramo prej namestiti program `wget`.


## Postopek

1. Izvršljivo datoteko `viu` prenesimo iz povezave [https://github.com/atanunq/viu/releases/download/v1.4.0/viu](https://github.com/atanunq/viu/releases/download/v1.4.0/viu) in jo shranimo v mapo `files`.

2. Odprimo datoteko [`firbec.def`](./firbec.def), ki jo bomo v nadaljevanju dopolnjevali.

3. V razdelku `%files` zahtevajmo kopiranje datoteke `/files/viu` z gostitelja v mapo `/exec/` v vsebniku.

4. Za nemoteno izvajanje programov v razdelku `%environment` nastavimo okoljsko spremenljivko
    
    ```shell
    export LC_ALL=C
    ```
    
    S tem preprečimo, da bi med namestitvijo programi od nas zahtevali vnašanje vrednosti. Nekateri programi med nameščanjem in delovanjem zahtevajo nastavitev lokalizacije. Univerzalna nastavitev je C (_angl. Computer_).
    
    Da nam pri zaganjanju programa `viu` ni treba vedno vnašati poti `/exec/viu`, dopolnimo okoljsko spremenljivko `PATH`

    ```shell
    export PATH=/exec:${PATH}
    ```

5. V razdelku `%post` najprej nastavimo okoljski spremenljivki `LC_ALL` (lokalizacija) in `DEBIAN_FRONTEND` za neinteraktivno nameščanje. Nato namestitvenemu programu `apt` posodobimo povezave do repozitorijev in namestimo program `wget`. Pri vsakem klicu programa `apt` dodamo stikalo `-y` - v primeru kakršnegakoli vprašanja bo `apt` avtomatsko izbral pritrdilni odgovor (_angl. yes_).

    ```shell
    export LC_ALL=C
    export DEBIAN_FRONTEND=noninteractive

    apt update -y
    apt install -y wget
    ```

    Prenesimo sliko in jo shranimo v mapo `/img`.

    ```shell
    wget -P /img https://www.izum.si/wp-content/uploads/2021/03/210322_VEGA_083.jpg
    ```

    Nazadnje nastavimo, da lahko vsakdo zažene program `viu` in odpre sliko.

    ```shell
    chmod a+rx /exec/viu
    chmod a+r /img/*
    ```    

6. Zdaj poskrbimo, da se pri zagonu vsebnika z ukazom `apptainer run` brez argumentov izriše shranjena slika in izpišejo kratka navodila za uporabo, pri zagonu z argumenti pa vsebnik le-te posreduje programu `viu`. Število argumentov v skripti podaja `$#`, vsi argumenti pa so označeni z `$@`

    ```shell
    if [ $# -eq 0 ]
    then
        viu /img/*
        echo "Kako uporabljam vsebnik ..."
    else
        viu $@
    fi

7. V razdeleku `%test` preverimo, če imamo v vsebniku na ustreznih lokacijah izvršljiv program `viu` in sliko `210322_VEGA_083.jpg`. V primeru, da program `test` programa ali datoteke ne bo našel, se bo zaključil z napako in ustavil gradnjo vsebnika.

    ```shell
    test -x /exec/viu
    test -f /img/210322_VEGA_083.jpg
    ```

8. V razdelek `%labels` dodamo oznake o vsebniku: `Author`, `Container`, `Version`, `Description` in v razadelek `%help` napišemo navodila za uporabo.

9. Vsebnik zgradimo in ga preverimo
    
    ```console
    $ apptainer build --fakeroot firbec.sif firbec.def

    $ apptainer test firbec.sif
    $ apptainer inspect firbec.sif
    $ apptainer run-help firbec.sif
    $ ./firbec.sif ./files/
    ```

10. V mapo `./extras` s spleta prenesmo nekaj slik. Nato zaženemo vsebnik tako, da mapo `./extras` povežemo z mapo `/img` v vsebniku. 

    ```console
    $ apptainer run --bind ./extras:/img firbec.sif
    ```

    Zdaj program izriše slike iz mape `./extras`, ne pa slik iz mape `/img`.

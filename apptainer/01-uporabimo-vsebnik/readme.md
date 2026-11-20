# Vaja 1: Uporabimo že pripravljen vsebnik

## Kaj bomo naredili?

V tej vaji ponovimo ukaze, objavljene v poglavju [Pomembni ukazi](). Uporabili bomo vsebnik, ki ga najdemo v repozitoriju [Docker Hub](https://hub.docker.com/r/sylabsio/lolcow). 

## Postopek
1. Najprej z ukazom `apptainer version` preverimo, da imamo ogrodje Apptainer nameščeno.

2. Odpremo spletno stran [Docker Hub](https://hub.docker.com/) in v polje za iskanje vpišemo **lolcow**. Izberemo zadnjo različico (latest)vsebnika, ki ga je pripravil uporabnik **sylabsio**: `docker://sylabsio/lolcow:latest`.

3. Vsebnik prenesemo na svoj računalnik

    ```console
    $ apptainer pull docker://sylabsio/lolcow:latest
    ```

4. Vsebnik zaženemo v interaktivnem načinu

    ```console
    $ apptainer shell lolcow_latest.sif
    ```

    - Preverimo, kaj nam izpišejo ukazi:      
        - `hostname`, 
        - `whoami`, 
        - `cat /etc/os-release`, 
        - `echo $PATH`, 
        - `ls`, 
        - `ls /usr/games`.
    - V vsebniku zaženimo ukaz `cowsay`, kot argument napišimo poljuben niz znakov.
    - Vsebino datoteke `/etc/os-release` skopirajmo v trenutno mapo na gostitelju v datoteko `lolcow-os.info`.      Uporabimo ukaz:
        ```console
        $ cp /etc/os-release ./lolcow-os.info
        ```
6. Z ukazom `exit` zapustimo vsebnik.

7. Z ukazom `apptainer exec` z gostitelja zaženemo ukaz v vsebniku. Preizkusimo nekaj spodnjih ukazov.
    ```console
    $ apptainer exec lolcow_latest.sif cowthink "Hmmmm..."
    
    $ apptainer exec lolcow_latest.sif lolcat ./lolcow-os.info
    ```

8. Vsebnik zaženemo še z nekaj različicami ukaza `apptainer run`.
    ```console
    $ apptainer run lolcow_latest.sif

    $ ./lolcow_latest.sif

    $ apptainer run docker://sylabsio/lolcow:latest
    ```

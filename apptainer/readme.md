# Vsebniki SingularityApptainer
Za vaje v tej mapi potrebujete ogrodje Appatiner. Najbolje je, da si ogrodje namestite na svoj osebni računalnik. Sledite [navodilom](https://apptainer.org/docs/user/main/quick_start.html). Med delavnico imate dostop do strežnika, na katerem imate vse potrebne pravice za delo z ogrodjem Apptainer.
<!---
Da vam bodo vsi primeri delovali, morate najprej dodati register vsebnikov cloud.sycloud.io. To storite tako, da na strežniku v ukazni vrstici zaženete spodnja dva ukaza:

```
$ apptainer remote add --no-login SylabsCloud cloud.sycloud.io
$ apptainer remote use SylabsCloud
```
-->

Seznam vaj:

- 01-uporabimo-vsebnik: naučimo se uporabiti že pripravljen vsebnik,
- 02-peskovnik: interaktivno zgradimo enostaven vsebnik za pregledovanje slik,
- 03-recept: pripravimo recept za gradnjo vsebnika za pregledovanje slike,
- 04-python-scilib: pripravimo recept za gradnjo vsebnika, ki vsebuje python in vse potrebne knjižnice za izris mandelbrotove množice,
- 05-mb-cpu: pripravimo vsebnik za zagon na procesorskih jedrih računskega vozlišča, ki izriše mandebrotovo množico,
- 06-mb-gpu: pripravimo vsebnik za izris mandelbrotove množice s pomočjo GPE
- 07-mb-mpi: pripravimo vsebnik za izris mandebrotove množice z uporabo knjižnice MPI in večih računskih vozlišč,
- 08-x: pripravimo vsebnik, ki omogoča uporabo protokola X za prikaz grafike na oddaljenem terminalu 

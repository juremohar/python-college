# 2.1 - Uvoz vhodnih podatkov

# 1.del - Sizh

thick = 2.0300
width = 5.0000
gauge_len = 50.0000

Sizh = [[thick, width, gauge_len]] * 5

# 2.del - Snt

Snt = list()
s1 = list()
s2 = list()
s3 = list()
s4 = list()
s5 = list()

d = open(".\\BenjaminPodlogar_NatezniTest_FTPO_CSV.csv", "r")
line = d.readline()

stevec = 0
while line and stevec < 3:  # s tem izpustimo prve tri vrstice in imamo samo podatke
    line = d.readline()
    stevec += 1

while line:
    index = 0
    index_zacetek = 0
    index_konec = 0
    stevilo = 0
    stevec = 1

    line = line.replace("\n", " ")
    line = line.replace(";", " ")
    line = line.replace(",", ".")
    line = line.replace("    ", " !")  # s tem izpustimo prazne celice v excelu

    while index < len(line):

        if line[index] == " ":
            index_konec = index
            stevilo = line[index_zacetek:index_konec]
            line = line.strip()
            index_zacetek = index_konec + 1

            ostanek = stevec % 4  # s tem vzamemo 1-3. podatke in izpustimo 4.ti podatek, ki je za nas nepomemben
            if ostanek != 0 and stevilo != "" and stevilo != "!":  # ko pride do praznih celic, s tem izpustimo motece ! in ""
                if stevec >= 1 and stevec < 4:  # s pomočjo stevca razvrstimo podatke za posamezno epruvetko v svoj podseznam
                    stevilo = float(stevilo)
                    s1.append(stevilo)
                if stevec >= 5 and stevec < 8:
                    stevilo = float(stevilo)
                    s2.append(stevilo)
                if stevec >= 9 and stevec < 12:
                    stevilo = float(stevilo)
                    s3.append(stevilo)
                if stevec >= 13 and stevec < 16:
                    stevilo = float(stevilo)
                    s4.append(stevilo)
                if stevec >= 17 and stevec < 20:
                    stevilo = float(stevilo)
                    s5.append(stevilo)

            stevec += 1

        if line[
            index] == "!":  # tukaj bomo stevec prestavili za +3 da recemo kot da so bile vrednosti da ohranimo sistem z zadnjimi stevilkami
            stevec += 3
        index += 1

    line = d.readline()
d.close()

Snt.append(s1)
Snt.append(s2)
Snt.append(s3)
Snt.append(s4)
Snt.append(s5)

# 2.2 - Izračun površine preseka vzorca
# 2.3 - Izračun natezne trdnosti
# 2.4 - Izračun raztezka

Sntrd = list()
Sraz = list()

i_podseznami = 0
index = 0

while i_podseznami < len(Snt):

    i_podatki1 = 1
    A = Sizh[index][1] * Sizh[index][
        0]  # se sprehodi s pomočjo indexa od prvega podseznama do petega in izračuna površine za vsako eprutevko (5 površin). [1]=width, [0]=thickness

    i_podatki2 = 2
    Gau_len = Sizh[index][
        2]  # se sprehodi s pomočjo indexa od prvega podseznama do petega in poda dolžino za vsako eprutevko (5 dolžin). [2]=gauge lenght

    zacasni_seznam1 = list()  # .clear pocisti tudi vrednosti v Sntrd, zato se raje zgenerira nov zacasni seznam
    zacasni_seznam2 = list()

    while i_podatki1 < len(Snt[i_podseznami]) and i_podatki2 < len(Snt[
                                                                       i_podseznami]):  # program bo deloval ko bo mesto podatka manjse od kolicine podatkov v podseznamu, kar bo vedno več.
        force = Snt[i_podseznami][
            i_podatki1]  # [i_podseznami] = index za podseznam, [i_podatki1] = index za podatek sile v podseznamu

        natezna_trdnost = force / A
        zacasni_seznam1.append(natezna_trdnost)

        stroke = Snt[i_podseznami][
            i_podatki2]  # [i_podseznami] = index za podseznam, [i_podatki2] = index za podatek dolžine

        raztezek = (((stroke + Gau_len) / Gau_len) - 1) * 100
        zacasni_seznam2.append(raztezek)

        i_podatki1 += 3  # s tem se prestavimo na naslednjo silo v podseznamu
        i_podatki2 += 3

    Sntrd.append(zacasni_seznam1)  # celoten zacasni seznam dodamo kot podseznam v Sntrd.
    Sraz.append(zacasni_seznam2)

    index += 1
    i_podseznami += 1

# 2.5 - Izračun povprečne natezne trdnosti in povprečnega raztezka

i_podseznami = 0
seznam_velikosti_podseznamov = list()  # da dobimo vrednosti dolžin vseh podseznamov

while i_podseznami < len(Sntrd):  # se sprehodimo cez dolzine podseznamov v seznamu nateznih trdnosti
    velikost_podseznama = len(Sntrd[i_podseznami])
    seznam_velikosti_podseznamov.append(velikost_podseznama)
    i_podseznami += 1

seznam_velikosti_podseznamov.sort()  # uredimo vrednosti dolzin po vrsti, da kasneje uporabimo zadnjo najvecjo kot pogoj

i_podseznami = 0
index = 0
seznam_z_enakimi_indexi_ntrd = list()
seznam_z_enakimi_indexi_raz = list()

while len(seznam_z_enakimi_indexi_ntrd) != seznam_velikosti_podseznamov[
    -1]:  # bo deloval tako dolgo dokler število podseznamov ne bo enako številu vrednosti v najdaljšem podseznamu epruvetk

    zacasni_seznam_ntrd = list()
    zacasni_seznam_raz = list()
    i_podseznami = 0

    while i_podseznami < len(Sntrd):
        if index < len(Sntrd[i_podseznami]):  # dolzina Sntrd in Sraz je enaka, tako da je lahko isti pogoj za oba
            stevilo_ntrd = Sntrd[i_podseznami][index]  # stevilo iz seznama natezne trdnosti
            stevilo_raz = Sraz[i_podseznami][index]  # stevilo iz seznama raztezka
            zacasni_seznam_ntrd.append(stevilo_ntrd)
            zacasni_seznam_raz.append(stevilo_raz)
        i_podseznami += 1
    index += 1
    seznam_z_enakimi_indexi_ntrd.append(zacasni_seznam_ntrd)
    seznam_z_enakimi_indexi_raz.append(zacasni_seznam_raz)

Sntrd_povp = list()  # seznama za povprecne vrednosti epruvetk
Sraz_povp = list()

i_podseznami = 0

while i_podseznami < len(seznam_z_enakimi_indexi_ntrd):
    povprecno_stevilo_ntrd = sum(seznam_z_enakimi_indexi_ntrd[i_podseznami]) / len(
        seznam_z_enakimi_indexi_ntrd[i_podseznami])  # izračuna povprečje podseznama
    povprecno_stevilo_raz = sum(seznam_z_enakimi_indexi_raz[i_podseznami]) / len(
        seznam_z_enakimi_indexi_raz[i_podseznami])
    Sntrd_povp.append(povprecno_stevilo_ntrd)
    Sraz_povp.append(povprecno_stevilo_raz)

    i_podseznami += 1

import matplotlib.pyplot as plt
import numpy as np

plt.plot(Sraz_povp, Sntrd_povp, label="Average Tensile Test", c="#C71585")
plt.title("Relationship between Stress and Strain (Tensile Test) - Average")
plt.xlabel("Strain (%) - Average")
plt.ylabel("Stress (MPa) - Average")
plt.legend()
plt.grid(linestyle="dotted")
plt.show()

# 2.6 Izris krivulj na graf

import matplotlib.pyplot as plt
import numpy as np

barve = ["#FF0000", "#8B4513", "#800080", "#008000", "#000080"]
epruvetke = ["1. Test", "2. Test", "3. Test", "4. Test", "5. Test"]

i_podseznami = 0
i_premik_grafa = 0

while i_podseznami < len(Sraz):  # se sprehodi čez vseh 5 epruvetk
    index = 0
    x = list()  # s tem počistimo seznam prejšnih vrednosti x in y
    y = list()
    while index < len(Sraz[i_podseznami]):  # se sprehodi čez vsako vrednost podseznama epruvetke
        x.append(Sraz[i_podseznami][
                     index] + i_premik_grafa)  # z i_premik_grafa prištejemo vsaki naslednji epruvetki +1, da bodo krivulje epruvetk ločene
        y.append(Sntrd[i_podseznami][index])

        index += 1

    plt.plot(x, y, label=epruvetke[i_podseznami],
             c=barve[i_podseznami])  # doda krivuljo s trenutnimi podatki za eno od epruvetkl. Label=doda ime krivulje

    i_podseznami += 1
    i_premik_grafa += 1

plt.title("Relationship between Stress and Strain (Tensile Test)")
plt.xlabel("Strain [%]")
plt.ylabel("Stress [MPa]")
plt.legend()
plt.grid(linestyle="dotted")
plt.show()


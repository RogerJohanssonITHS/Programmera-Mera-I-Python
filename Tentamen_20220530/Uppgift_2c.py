# -*- coding: utf-8 -*-
"""
Created on Wed May 25 13:20:00 2022

@author: S2200132
"""

# Återanvänd Mynt-klassen från b) och skriv en egendefinierad
# funktion slantsingling() som tar ett Mynt-objekt som argument.
# Funktionen ska först som likt i b) fråga användaren efter antal kast,
# räkna utfallen och skriva ut resultatet. Resultatet ska sen även presenteras
# i ett stapeldiagram med matplotlib.
# Skapa ett Mynt-objekt i huvudprogrammet att provanropa din
# slantsingling()-funktion med.

# importera moduler
import matplotlib.pyplot as plt
import random


# klassen Mynt
class Mynt:
    def __init__(self, sidaupp=""):
        self.singling(sidaupp)

    def singling(self, sidaupp):
        myntsidor = ["Krona", "Klave"]
        slumptalet = random.randint(0, 1)
        self.__sidaupp = (myntsidor[slumptalet])
        return

    def get_sidaupp(self):
        return self.__sidaupp


# funktion som utför simuleringen och anropar funktionen "plottaresultatet"
# för att skapa ett stapeldiagram
def slantsingling(mynt):
    # be om antal kast som skall utföras
    antalKast = int(input("Skriv in antal kast som ska simuleras: "))
    print(f'Tack, jag kastar myntet {antalKast} gånger:')

    # genomför simuleringen och skriv ut resultatet
    antalKrona = 0
    antalKlave = 0
    for i in range(antalKast):
        mynt.singling("")
        status = mynt.get_sidaupp()
        if status == "Krona":
            antalKrona += 1
        else:
            antalKlave += 1
    print(f'Utfallet blev {antalKrona} för Krona och {antalKlave} för Klave.')
    plottaresultatet(antalKrona, antalKlave)


# metod som skapar ett stapeldiagram för utfallet av slantsinglingarna
def plottaresultatet(antalKrona, antalKlave):
    # sätter attributen för grafen
    myntsidor = ["Klave", "Krona"]
    utfall = [antalKlave, antalKrona]
    plt.grid()
    plt.xlabel('Antal')
    plt.ylabel('Utfall')
    plt.title("Visar antal utfall av Krona och Klave")
    plt.barh(myntsidor, utfall, color=['b', 'r'])
    plt.show()


# huvudprogram
mittMynt = Mynt()
slantsingling(mittMynt)

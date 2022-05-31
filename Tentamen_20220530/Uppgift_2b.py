# -*- coding: utf-8 -*-
"""
Created on Wed May 25 13:20:00 2022

@author: S2200132
"""

# Skapa en klass Mynt som kan simulera slantsingling med de två utfallen krona
# och klave genom att använda modulen random. Kalla variabeln i klassen som
# håller koll på myntets nuvarande visade sida (krona eller klave) för sidaupp.
# Gör variabeln privat genom name mangling och skriv en get-metod för den.
# Slumpkoden för singlingen ska ligga i en metod singling().

# Skriv sen ett huvudprogram som först skapar ett Mynt-objekt och skriver ut
# vilken sida myntet först har efter den godtyckliga start-tilldelningen.
# Sen ska användaren tillfrågas hur många antal kast som önskas simuleras,
# varav det sen utförs och antal utfall av respektive sort räknas.

# importera moduler
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


# huvudprogram
# skapa nytt mynt och skriv ut status
mittmynt = Mynt()
print(f'Nytt mynt skapat. Denna sida är upp just nu: {mittmynt.get_sidaupp()}')

# be om antal kast som skall utföras
antalKast = int(input("Skriv in antal kast som ska simuleras: "))
print(f'Tack, jag kastar myntet {antalKast} gånger:')

# genomför simuleringen och skriv ut resultatet
antalKrona = 0
antalKlave = 0
for i in range(antalKast):
    mittmynt.singling("")
    status = mittmynt.get_sidaupp()
    if status == "Krona":
        antalKrona += 1
    else:
        antalKlave += 1
print(f'Utfallet blev {antalKrona} för Krona och {antalKlave} för Klave.')

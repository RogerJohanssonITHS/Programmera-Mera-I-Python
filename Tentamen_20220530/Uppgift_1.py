# -*- coding: utf-8 -*-
"""
Created on Wed May 25 13:20:00 2022

@author: S2200132
"""

# importera moduler
import numpy as np


# ingående data till uppgift 1

data = [[0., 0.2, 0.4, 0.6, 0.8, 1., 1.2, 1.4, 1.6, 1.8],

        [2., 2.2, 2.4, 2.6, 2.8, 3., 3.2, 3.4, 3.6, 3.8],

        [4., 4.2, 4.4, 4.6, 4.8, 5., 5.2, 5.4, 5.6, 5.8],

        [6., 6.2, 6.4, 6.6, 6.8, 7., 7.2, 7.4, 7.6, 7.8],

        [8., 8.2, 8.4, 8.6, 8.8, 9., 9.2, 9.4, 9.6, 9.8]]

# skapa NP_A
NP_A = np.array(data)

# deluppgift a). Extrahera [[4.2 4.6]
#                         [6.2 6.6]]
# ur NP_A genom att använda metoden slicing och skriv ut resultatet.
# Spara den som NP_C.

NP_C = NP_A[2:4:1, 1:4:2]
print(NP_C)


# deluppgift b). Skriv ut alla element i NP_A
# som är större än 3 men mindre än 4.
resultatB = NP_A[(NP_A > 3) & (NP_A < 4)]
print("Tal i NP_A som är större än 3 och mindre än 4: ", resultatB)


# deluppgift c). Skapa två listor, en med maxvärdet från varje rad och en med
# maxvärdet från varje kolumn i NP_A och skriv ut resultatet.

maxValuesRow = np.amax(NP_A, axis=1)
maxValuesCol = np.amax(NP_A, axis=0)

print("De högsta värdena i NP_As kolumner är: ", maxValuesCol)
print("De högsta värdena i NP_As rader är:", maxValuesRow)


# deluppgift d). Man kan använda funktionen array_split() för dela upp
# en Numpy-array i olika sub-Numpy-arrayer. Använd denna funktion för att dela
# NP_A i 5st sub-Numpy-arrayer och skriv ut resultatet.

NP_A_split = np.array_split(NP_A, 5)
print(NP_A_split)


# deluppgift e). Tillämpa funktionen where() på NP_A för att byta ut
# alla element i NP_A som är större än 8 till talet 11.
# Skriv ut den modifierade Numpy-arrayen.

print(np.where(NP_A > 8, 11, NP_A))


# deluppgift f). Omvandla NP_A till en vektor (endimensionell Numpy-array)
# och skriv ut resultatet.

print(NP_A.flatten())


# deluppgift g). Transponera NP_C från a) och kalla den transponerade
# Numpy-arrayen NP_CT. Utför därefter beräkningen (subtraktionen) NP_CT - NP_C
# och skriv ut resultatet.
# Beskriv med egna ord i en kommentar vad processen gör.

NP_CT = NP_C.transpose()
print(NP_CT - NP_C)

# Egen kommentar: tranponatet av NP_C erhålls genom att byta rader mot kolumner
# och kolumner mot rader. I fallet av en 2x2-matris behåller man värdena längs
# diagonalen från övre vänstra till nedre högra hörnet och byter plats på
# övriga värden.

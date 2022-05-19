# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 12:50:51 2022

"""


# Skriv ett program som beräknar trafikintensiteten timma för timma för den
# mätplats som har flest passerande fordon under mätperioden.
# Skapa därefter ett stapeldiagram med upplösningen 1 h över antal fordon som
# passerar kameran mellan kl. 07:00 och 18:00.
# Klockslag på x-axeln och antalet fordon på y-axeln.

# importera moduler
import pandas as pd
import matplotlib.pyplot as plt

# läs in csv-filer. Ge felmeddelande om de ej ligger i samma mapp.
fileFound = False
while not fileFound:
    try:
        platsdata = pd.read_csv('platsData.csv', encoding='ISO-8859-1', sep=';')
        kameradata = pd.read_csv('kameraData.csv', encoding='ISO-8859-1', sep=';')
        fileFound = True
    except (FileNotFoundError, IOError):
        print("Placera csv-filerna i samma mapp som programfilen")
        input("Tryck på 'Retur' för att fortsätta")


# Hitta trafikplatsen med högst antal passerande fordon under mätperioden
matplatsMaxAntalFordon = kameradata.groupby('MätplatsID').\
    size().agg(['idxmax', 'max'])

# konvertera kolumnen Tid till ett datetime-objekt
kameradata['Tid'] = pd.to_datetime(kameradata['Tid'])

# skapa lista med antalet fordon per timma
antalFordonPerTimma = []

# populera listan antalFordonPerTimma
for timma in range(7, 18):
    mask = (kameradata['Tid'].dt.hour >= timma) & \
        (kameradata['Tid'].dt.hour < timma + 1) & \
        (kameradata['MätplatsID'] == matplatsMaxAntalFordon[0])
    antalFordonPerTimma.append(kameradata[mask]['Tid'].count())

# hämta data för mätplatsen
matplatsBeskrivning = platsdata[platsdata['MätplatsID'] == matplatsMaxAntalFordon[0]]

pltTitel = "Antal fordon som kamerorna registrerat i " + matplatsBeskrivning.iat[0, 1] \
    + " - väg" + matplatsBeskrivning.iat[0, 2] \
    + "\ni " + matplatsBeskrivning.iat[0, 3] + " under perioden 2021-09-11 kl.07.00 - 18.00"

# sätter attributen för grafen
klockslagEtiketter = ['8:00', '9:00', '10:00', '11:00', '12:00', '13:00',
                      '14:00', '15:00', '16:00', '17:00', '18:00']
plt.xticks(rotation=45)
plt.grid()
plt.xlabel('Klockslag')
plt.ylabel('Antal fordon')
plt.title(pltTitel)
plt.bar(klockslagEtiketter, antalFordonPerTimma, color='r')
plt.show()

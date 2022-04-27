# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 18:00:59 2022

"""

# importera moduler
import pandas as pd
import matplotlib.pyplot as plt

# läs in csv-fil
kameradata = pd.read_csv('kameraData.csv', encoding='ISO-8859-1', sep=';')
# pafoljd = pd.read_csv('pafoljd.csv', encoding='ISO-8859-1', sep=';')
# platsdata = pd.read_csv('platsData.csv', encoding='ISO-8859-1', sep=';')

# Skapa ett program som beräknar summan av antal fordon som kamerorna har
# registrerat över alla mätplatser uppdelat per timma mellan kl. 07:00 och 18:00.

# konvertera kolumnen Tid till ett datetime-objekt
kameradata['Tid'] = pd.to_datetime(kameradata['Tid'])

# skapa lista med antalet fordon per timma
antalFordonPerTimma = []

# populera listan antalFordonPerTimma
for timma in range(7, 18):
    mask = (kameradata['Tid'].dt.hour >= timma) & \
        (kameradata['Tid'].dt.hour < timma + 1)
    antalFordonPerTimma.append(kameradata[mask]['Tid'].count())

# Skapa därefter ett linjediagram över resultatet där x-axeln är graderad
# i timmar mellan 07.00 och 18.00 och y-axeln i antal registrerade fordon.

# Rubrik: Totalt antal fordon som kamerorna registrerar i mätområdet 2021-09-11
# Y-axel: Antal fordon
# X-axel: Klockslag
# sätter attributen för grafen
klockslagEtiketter = ['8:00', '9:00', '10:00','11:00', '12:00', '13:00', '14:00','15:00', '16:00', '17:00', '18:00']
plt.xticks(rotation=45)
plt.xlabel('Klockslag')
plt.ylabel('Antal fordon')
plt.title('Totalt antal fordon som kamerorna registrerar i mätområdet 2021-09-11')
plt.plot(klockslagEtiketter, antalFordonPerTimma, color='r')
plt.show()

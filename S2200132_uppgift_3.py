# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 20:56:54 2022

"""

# importera moduler
import pandas as pd

# läs in csv-fil
kameradata = pd.read_csv('kameraData.csv', encoding='ISO-8859-1', sep=';')
pafoljd = pd.read_csv('pafoljd.csv', encoding='ISO-8859-1', sep=';')
platsdata = pd.read_csv('platsData.csv', encoding='ISO-8859-1', sep=';')

# Skriv ett program som först frågar efter en kommun och därefter skapar
# en tabell enligt nedan som innehåller de hastighetsöverträdelser som
# kamerorna registrerat under hela mätperioden.

# fråga efter kommunnamn tills giltigt namn anges
# inmatadKommun = input("Skriv in kommun: ")
inmatadKommun = 'Alingsås'
# hitta kameraId från platsdata genom kommunnamnet

# labbar med merge
mergedKameraPlatsData = pd.merge(kameradata, platsdata, how='inner', left_on = 'MätplatsID', right_on = 'MätplatsID')
pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', 100)

mergedKPDGrouped = mergedKameraPlatsData.groupby(['Kommun', 'Vägnummer'])

# print(mergedKameraPlatsData.head())
# mask = mergedKameraPlatsData['Kommun'] == 'Alingsås'
# print(mergedKameraPlatsData[mask]['Hastighet'].max())


for keys in mergedKPDGrouped.groups.keys():
    if keys[0] == inmatadKommun:
        # keys[1] ger vägnumret
        maxUppmattHast = mergedKPDGrouped.get_group(keys).max()
        print(maxUppmattHast)


# Konstruera tabellen
print('==================================================================================================\n')
print(f'{"" : <10}{"Kameraregistrerade hastighetsöverträdelser i": ^50} {"KOMMUNNAMN"}\n')
print(f'{"" : <10}{"2021-09-11 kl.0700-18.00": ^50}\n')
print(f'{"Vägnummer":<20} {"Max hastighet (km/h)":<20} {"Överträdelser (%)":<20} {"Högsta uppmätta ---":<20} {"Tidpunkt":>20}')
print(f'{"":<20} {"":<20} {"":<20} {"hastighet (km/h)":<20} {"":>20}')
print('--------------------------------------------------------------------------------------------------\n')

# ta fram tabellinnehåll

print('==================================================================================================\n')


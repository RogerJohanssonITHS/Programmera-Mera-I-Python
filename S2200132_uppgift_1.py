# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 13:35:48 2022

"""

# importera moduler
import pandas as pd

# läs in csv-filer
kameradata = pd.read_csv('kameraData.csv', encoding='ISO-8859-1', sep=';')
pafoljd = pd.read_csv('pafoljd.csv', encoding='ISO-8859-1', sep=';')
platsdata = pd.read_csv('platsData.csv', encoding='ISO-8859-1', sep=';')

# gruppera datan på Kommun och Vägnummer
platsdataGrupperadKommunVag = platsdata.groupby(['Kommun', 'Vägnummer'])

# Konstruera tabellen
print(f'{"" : <10}{"Hastighetsövervakning i Västra Götaland": ^50}\n')
print(f'{"Kommun":<20} {"Vägnummer":<20} {"Antal kameror":>5}')
print('============================================================\n')

kommun = ""  # variabel som innehåller det senast utskrivna kommunnamnet
for keys in platsdataGrupperadKommunVag.groups.keys():
    antalKameror = platsdataGrupperadKommunVag.get_group(keys)['Kommun'].count()
    if kommun == keys[0]:  # skriv inte ut kommunnamnet om det var samma som förra
        print(f'{"":<20} {keys[1]:<20} {antalKameror:>5}')
    else:
        print(f'{keys[0]:<20} {keys[1]:<20} {antalKameror:>5}')
    kommun = keys[0]
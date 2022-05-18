# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 13:35:48 2022

"""
# Skriv ett program som grupperar kamerorna per kommun och vägnummer.
# Tabellen ska innehålla kommun, vägnummer, antal kameror som finns
# installerade på detta vägnummer.

# importera moduler
import pandas as pd

# läs in csv-fil. Ge felmeddelande om den ej ligger i samma mapp.
fileFound = False
while not fileFound:
    try:
        platsdata = pd.read_csv('platsData.csv', encoding='ISO-8859-1', sep=';')
        fileFound = True
    except (FileNotFoundError, IOError):
        print("Placera csv-filen i samma mapp som programfilen")
        input("Tryck på 'Retur' för att fortsätta")


# gruppera datan på Kommun och Vägnummer
platsdataGrupperadKommunVag = platsdata.groupby(['Kommun', 'Vägnummer'])

# Konstruera tabellen
print(f'{"" : <10}{"Hastighetsövervakning i Västra Götaland": ^50}\n')
print(f'{"Kommun":<20} {"Vägnummer":<20} {"Antal kameror":>5}')
print('============================================================\n')

kommun = ""  # variabel som innehåller det senast utskrivna kommunnamnet
for keys in platsdataGrupperadKommunVag.groups.keys():
    antalKameror = platsdataGrupperadKommunVag.\
                get_group(keys)['Kommun'].count()
    if kommun == keys[0]:  # skriv inte ut kommunnamnet om det repeteras
        print(f'{"":<20} {keys[1]:<20} {antalKameror:>5}')
    else:
        print(f'{keys[0]:<20} {keys[1]:<20} {antalKameror:>5}')
    kommun = keys[0]

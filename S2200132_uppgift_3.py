# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 20:56:54 2022
"""
# Uppgift 3a

# Skriv ett program som först frågar efter en kommun och därefter skapar
# en tabell som innehåller de hastighetsöverträdelser som kamerorna
# registrerat under hela mätperioden.


# importera moduler
import pandas as pd
import numpy as np

# läs in csv-filer. Ge felmeddelande om de ej ligger i samma mapp.
fileFound = False
while not fileFound:
    try:
        kameradata = pd.read_csv('kameraData.csv', encoding='ISO-8859-1', sep=';')
        pafoljd = pd.read_csv('pafoljd.csv', encoding='ISO-8859-1', sep=';')
        platsdata = pd.read_csv('platsData.csv', encoding='ISO-8859-1', sep=';')
        fileFound = True
    except (FileNotFoundError, IOError):
        print("Placera csv-filerna i samma mapp som programfilen")
        input("Tryck på 'Retur' för att fortsätta")


# fråga efter kommunnamn tills giltigt namn anges
giltigKommun = False
while not (giltigKommun):
    inmatadKommun = input("Skriv in kommun i Västergötland (som exv. Tibro): ")
    for i in range(len(platsdata.Kommun)):
        if inmatadKommun == platsdata.Kommun[i]:
            print("Kommunen finns i databasen")
            giltigKommun = True
            break
    if not (giltigKommun):
        print("Ingen giltig kommun. Försök igen!\n")

# hitta kameraId från platsdata genom kommunnamnet
kameraPlatsData = pd.merge(kameradata, platsdata, how='inner',
                                 left_on='MätplatsID', right_on='MätplatsID')

grupperadKameraPlatsData = kameraPlatsData.groupby(['Kommun', 'Vägnummer'])

# ordna med genitiv-s på kommunnamnet och lägg till kommun
if inmatadKommun[-1] != "s":
    inmatadKommunGenitiv = inmatadKommun + "s" + " kommun"
else:
    inmatadKommunGenitiv = inmatadKommun + " kommun"

# Konstruera tabellen
print('===================================================================='
      '========================================\n')
print(f'{"" : <10}{"Kameraregistrerade hastighetsöverträdelser i":<10} {inmatadKommunGenitiv:<40}')
print(f'{"" : <10}{"2021-09-11 kl.0700-18.00": ^50}\n')
print(f'{"Vägnummer":<20} {"Max hastighet (km/h)":<20} {"Överträdelser (%)":<20} {"Högsta uppmätta ---":<20} {"Tidpunkt":>20}')
print(f'{"":<20} {"":<20} {"":<20} {"hastighet (km/h)":<20} {"":>20}')
print('--------------------------------------------------------------------'
      '----------------------------------------\n')

# ta fram tabellinnehåll
# keys i grupperadKameraPlatsData är Kommun och Vägnummer
for keys in grupperadKameraPlatsData.groups.keys():
    if keys[0] == inmatadKommun:
        # få fram objektet med högst uppmätt hastighet för aktuell kommun.
        # För det objektet ta fram gällande hastighet och tidpunkt
        maxUppmattHastObjekt = grupperadKameraPlatsData.get_group(keys).max()
        gallandeHastighet = maxUppmattHastObjekt['Gällande Hastighet']
        maxUppmattHastighet = maxUppmattHastObjekt['Hastighet']
        tidpunkt = maxUppmattHastObjekt['Tid']

        # räkna antalet uppmätta hastigheter och antalet uppmätta hastigheter
        # som ligger över gällande hastighetsgräns. Detta ger överträdelser.
        antalUppmattHast = grupperadKameraPlatsData.get_group(keys)['Datum'].count()
        antalUppmattHastOver = grupperadKameraPlatsData.get_group(keys)[grupperadKameraPlatsData.
                get_group(keys)['Hastighet'] > gallandeHastighet]['Tid'].count()
        overtradelser = round((antalUppmattHastOver/antalUppmattHast) * 100, 1)
        print(f'{keys[1]:<20} {gallandeHastighet:<20} {overtradelser:<20} {maxUppmattHastighet:<20} {tidpunkt:>20}')


print('===================================================================='
      '========================================\n')

# Uppgift 3b

# Utgå ifrån programmet i uppgift 3a och modifiera detta och skapa en ny tabell
# enligt nedan som skriver ut antalet böter och indragna körkort som utfärdats
# per vägnummer under mätperioden i den kommun som angavs i uppg 3a.


# Konstruera tabellen
print('===================================================================='
      '========================================\n')
print(f'{"" : <10}{"Påföljder vid kameraregistrerade hastighetsöverträdelser i":<10} {inmatadKommunGenitiv:<40}')
print(f'{"" : <10}{"2021-09-11 kl.0700-18.00": ^50}\n')
print(f'{"Vägnummer":<20} {"Max hastighet (km/h)":<20} {"Uppmätt hastighet":<20} {"Tidpunkt":<20} {"Påföljd":>20}')
print('--------------------------------------------------------------------'
      '----------------------------------------\n')

# ta fram tabellinnehåll
# gör om pafoljd till panda.Series
granser = pafoljd['Hastighetsöverträdelse (km/h)'].squeeze()
straffSatser = pafoljd['Påföljd'].squeeze()

# keys i grupperadKameraPlatsData är Kommun och Vägnummer
for keys in grupperadKameraPlatsData.groups.keys():
    if keys[0] == inmatadKommun:
        # ta fram de mätpunkter då den uppmätta hastigheten
        # överstiger den gällande hastigheten
        uppmattHastOver = grupperadKameraPlatsData.\
            get_group(keys)[grupperadKameraPlatsData.get_group(keys)['Hastighet'] > gallandeHastighet]
        
        # zippa hastigheter och tidpunkter från ovanstående funna mätpunkter
        hastigheter = uppmattHastOver['Hastighet'].values
        tidpunkter = uppmattHastOver['Tid'].values
        hastighetTidpunkt = zip(hastigheter, tidpunkter)
        
        # hitta idx för straffsatsen
        for hastighet, tidpunkt in hastighetTidpunkt:
            idx = np.argmax(granser >= hastighet - gallandeHastighet)
            print(f'{keys[1]:<20} {gallandeHastighet:<20} {hastighet:<20} {tidpunkt:<20} {straffSatser[idx]:>20}')

print('===================================================================='
      '========================================\n')
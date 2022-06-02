# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 13:25:21 2022

"""

# importera moduler
import pandas as pd


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


# ta fram tabellinnehåll
# slå ihop kameradata med platsdata via MätplatsID och
# gruppera på Kommun och vägnummer
kameraPlatsData = pd.merge(kameradata, platsdata, how='inner',
                                 left_on='MätplatsID', right_on='MätplatsID')

grupperadKameraPlatsData = kameraPlatsData.groupby(['MätplatsID', 'Kommun', 'Vägnummer'])

# skapa en behållare för tabellen
# tabellens principiella utseende blir:
# Kolumn 1 är key[1] dvs Kommun från grupperadKameraPlatsData
# Kolumn 2 är key[2] dvs Vägnummer från grupperadKameraPlatsData
# Kolumn 3 blir antalet uppmätta hastigheter
# Kolumn 4 blir antalet uppmätta hastighetsöverträdelser
tabell = []
for key in grupperadKameraPlatsData.groups.keys():
    gallandeHastighetObj = grupperadKameraPlatsData.\
        get_group(key)['Gällande Hastighet'].to_numpy()
    kommun = grupperadKameraPlatsData.get_group(key)['Kommun']
    gallandeHastighet = gallandeHastighetObj[0]
    antalUppmattHast = grupperadKameraPlatsData.get_group(key)['Datum'].count()
    antalUppmattHastOver = grupperadKameraPlatsData.\
        get_group(key)[grupperadKameraPlatsData.get_group(key)['Hastighet'] > gallandeHastighet]['Tid'].count()
    # overtradelser = round((antalUppmattHastOver/antalUppmattHast) * 100, 1)
    # spara till en tabell
    tabell.append([key[1], key[2], antalUppmattHast, antalUppmattHastOver])

# summera över kommun och vägnummer och beräkna procentuella andelen överträdelser.
df_tabell = pd.DataFrame(tabell, columns=['Kommun', 'Vägnummer', 'Antal fordon', 'Antal överträdelser'])

df_tabell_summor = df_tabell.groupby(['Kommun','Vägnummer'])['Antal fordon', 'Antal överträdelser'].sum()

# lägg till kolumn för procentuella andelen överträdelser i procent
df_tabell_summor['Andel överträdelser'] = df_tabell_summor['Antal överträdelser']/df_tabell_summor['Antal fordon'] * 100

# sortera i storleksordning på Kommun och Vägnummer
df_tabell_summor_sorted = df_tabell_summor.groupby(['Kommun', 'Vägnummer'])[['Andel överträdelser']].\
    max().sort_values('Andel överträdelser', ascending=False).reset_index()

# spara bara första raden för varje kommun (innehåller högsta värdet för Andel överträdelser)
df_gallrad = df_tabell_summor_sorted.drop_duplicates(subset=['Kommun'])

# avrunda värdena i kolumnen Andel överträdelser till en decimal
df_gallrad['Andel överträdelser'] = df_gallrad['Andel överträdelser'].round(decimals=1)

# Konstruera tabellen
print('==================================================================='
      '=========================================\n')
print(f'{"Det vägnummer inom respektive kommun där kameran registrerat procentuellt flest"}')
print(f'{"" : <7}{"hastighetsöverträdelser under perioden 2021-09-11 kl.07.00-18.00"}\n')
print(f'{"Kommun":<20} {"Vägnummer":<20} {"Överträdelser (%)":<20}')
print('-------------------------------------------------------------------'
      '-----------------------------------------\n')
for i in range(len(df_gallrad)):
    print(f'{df_gallrad.iloc[i, 0]:<20} {df_gallrad.iloc[i, 1]:<20} {df_gallrad.iloc[i, 2]:<20}')
print('==================================================================='
      '=========================================\n')

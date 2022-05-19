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
# Kolumn 3 blir andelen överträdelser som beräknas nedan
tabell = []
for key in grupperadKameraPlatsData.groups.keys():
    gallandeHastighetObj = grupperadKameraPlatsData.\
        get_group(key)['Gällande Hastighet'].to_numpy()
    kommun = grupperadKameraPlatsData.get_group(key)['Kommun']
    gallandeHastighet = gallandeHastighetObj[0]
    antalUppmattHast = grupperadKameraPlatsData.get_group(key)['Datum'].count()
    antalUppmattHastOver = grupperadKameraPlatsData.\
        get_group(key)[grupperadKameraPlatsData.get_group(key)
                       ['Hastighet'] > gallandeHastighet]['Tid'].count()
    overtradelser = round((antalUppmattHastOver/antalUppmattHast) * 100, 1)
    # spara till en tabell
    tabell.append([key[1], key[2], overtradelser])


# gallra tabellen och sortera i storleksordning
df_tabell = pd.DataFrame(tabell, columns=['Kommun', 'Vägnummer', 'Överträdelser'])
df_tabell_grouped_sorted = df_tabell.groupby(['Kommun'])[['Vägnummer', 'Överträdelser']].\
    max().sort_values('Överträdelser', ascending=False).reset_index()
# Konstruera tabellen
print('==================================================================='
      '=========================================\n')
print(f'{"Det vägnummer inom respektive kommun där kameran registrerat procentuellt flest"}')
print(f'{"" : <7}{"hastighetsöverträdelser under perioden 2021-09-11 kl.07.00-18.00"}\n')
print(f'{"Kommun":<20} {"Vägnummer":<20} {"Överträdelser (%)":<20}')
print('-------------------------------------------------------------------'
      '-----------------------------------------\n')
for i in range(len(df_tabell_grouped_sorted)):
    print(f'{df_tabell_grouped_sorted.iloc[i, 0]:<20} {df_tabell_grouped_sorted.iloc[i, 1]:<20} {df_tabell_grouped_sorted.iloc[i, 2]:<20}')
print('==================================================================='
      '=========================================\n')







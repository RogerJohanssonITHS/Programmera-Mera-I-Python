# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 13:25:21 2022

"""

# importera moduler
import pandas as pd
import numpy as np

# läs in csv-fil
kameradata = pd.read_csv('kameraData.csv', encoding='ISO-8859-1', sep=';')
pafoljd = pd.read_csv('pafoljd.csv', encoding='ISO-8859-1', sep=';')
platsdata = pd.read_csv('platsData.csv', encoding='ISO-8859-1', sep=';')

# Konstruera tabellen
print('============================================================================================================\n')
print(f'{"Det vägnummer inom respektive kommun där kameran registrerat procentuellt flest"}')
print(f'{"" : <7}{"hastighetsöverträdelser under perioden 2021-09-11 kl.07.00-18.00"}\n')
print(f'{"Kommun":<20} {"Vägnummer":<20} {"Överträdelser (%)":<20}')
print('------------------------------------------------------------------------------------------------------------\n')

# ta fram tabellinnehåll
# Skapa en tabell enligt nedan som innehåller samtliga kommuner i mätningen
# tillsammans med det vägnumret i respektive kommun som har procentuellt högst
# antal hastighetsöverträdelser*.
# Den kommun med flest överträdelser ska stå överst i tabellen osv.
# Tabellen ska innehålla följande kolumner:
# Kommun, vägnummer, procentuellt antal registrerade hastighetsöverträdelser.

# slå ihop kameradata med platsdata via MätplatsID och
# gruppera på Kommun och vägnummer
mergedKameraPlatsData = pd.merge(kameradata, platsdata, how='inner',
                                 left_on='MätplatsID', right_on='MätplatsID')

mergedKPDGrouped = mergedKameraPlatsData.groupby(['MätplatsID', 'Kommun', 'Vägnummer'])

# skapa en behållare för tabellen
tabell = []
for key in mergedKPDGrouped.groups.keys():
    # print(key)
    gallandeHastighetObj = mergedKPDGrouped.get_group(key)['Gällande Hastighet'].to_numpy()
    # print(gallandeHastighetObj)
    # print(type(gallandeHastighetObj))
    kommun = mergedKPDGrouped.get_group(key)['Kommun']
    # print(kommun)
    gallandeHastighet = gallandeHastighetObj[0]
    # print(gallandeHastighet)
    # print(type(gallandeHastighet))
    antalUppmattHast = mergedKPDGrouped.get_group(key)['Datum'].count()
    antalUppmattHastOver = mergedKPDGrouped.get_group(key)[mergedKPDGrouped.get_group(key)['Hastighet']>gallandeHastighet]['Tid'].count()
    overtradelser = round((antalUppmattHastOver/antalUppmattHast) * 100, 1)
    # spara till en tabell
    tabell.append([key[1], key[2], overtradelser])
    # print(f'{key[1]:<20} {key[2]:<20} {overtradelser:<20}\n')

print('============================================================================================================\n')
print(tabell)
# gallra tabellen och sortera i storleksordning
# skapa dataframe
df_tabell = pd.DataFrame(tabell, columns=['Kommun', 'Vägnummer', 'Överträdelser'])
print(df_tabell)
df_tabell_grouped = df_tabell.groupby(['Kommun', 'Vägnummer'])
df_tabell_grouped_max = df_tabell_grouped['Överträdelser'].max()
print(df_tabell_grouped_max)


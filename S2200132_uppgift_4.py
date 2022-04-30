# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 13:25:21 2022

"""

# importera moduler
import pandas as pd

# läs in csv-fil
kameradata = pd.read_csv('kameraData.csv', encoding='ISO-8859-1', sep=';')
pafoljd = pd.read_csv('pafoljd.csv', encoding='ISO-8859-1', sep=';')
platsdata = pd.read_csv('platsData.csv', encoding='ISO-8859-1', sep=';')


# ta fram tabellinnehåll
# slå ihop kameradata med platsdata via MätplatsID och
# gruppera på Kommun och vägnummer
mergedKameraPlatsData = pd.merge(kameradata, platsdata, how='inner',
                                 left_on='MätplatsID', right_on='MätplatsID')

mergedKPDGrouped = mergedKameraPlatsData.groupby(['MätplatsID', 'Kommun', 'Vägnummer'])

# skapa en behållare för tabellen
tabell = []
for key in mergedKPDGrouped.groups.keys():
    gallandeHastighetObj = mergedKPDGrouped.get_group(key)['Gällande Hastighet'].to_numpy()
    kommun = mergedKPDGrouped.get_group(key)['Kommun']
    gallandeHastighet = gallandeHastighetObj[0]
    antalUppmattHast = mergedKPDGrouped.get_group(key)['Datum'].count()
    antalUppmattHastOver = mergedKPDGrouped.get_group(key)[mergedKPDGrouped.get_group(key)['Hastighet']>gallandeHastighet]['Tid'].count()
    overtradelser = round((antalUppmattHastOver/antalUppmattHast) * 100, 1)
    # spara till en tabell
    tabell.append([key[1], key[2], overtradelser])


# gallra tabellen och sortera i storleksordning
df_tabell = pd.DataFrame(tabell, columns=['Kommun', 'Vägnummer', 'Överträdelser'])
df_tabell_grouped_sorted = df_tabell.groupby(['Kommun'])\
[['Vägnummer', 'Överträdelser']].max().sort_values('Överträdelser', ascending=False).reset_index()
print(df_tabell_grouped_sorted)
print(type(df_tabell_grouped_sorted))
# Konstruera tabellen
print('============================================================================================================\n')
print(f'{"Det vägnummer inom respektive kommun där kameran registrerat procentuellt flest"}')
print(f'{"" : <7}{"hastighetsöverträdelser under perioden 2021-09-11 kl.07.00-18.00"}\n')
print(f'{"Kommun":<20} {"Vägnummer":<20} {"Överträdelser (%)":<20}')
print('------------------------------------------------------------------------------------------------------------\n')
for i in range(len(df_tabell_grouped_sorted)):
    print(f'{df_tabell_grouped_sorted.iloc[i, 0]:<20} {df_tabell_grouped_sorted.iloc[i, 1]:<20} {df_tabell_grouped_sorted.iloc[i, 2]:<20}')
print('============================================================================================================\n')







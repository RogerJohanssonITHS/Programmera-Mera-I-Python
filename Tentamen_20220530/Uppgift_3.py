# -*- coding: utf-8 -*-
"""
Created on Wed May 25 13:20:00 2022

@author: S2200132
"""

# deluppgift a). Skriv kod som läser in innehållet i
# Temperaturdata_Abisko_2019.csv till ett pandas-DataFrame-objekt
# med namnet df_temp_Abisko.
# Gör motsvarande för csv-filen Temperaturdata_Lund_2019.csv och lagra dess
# innehåll i ett DataFrame-objekt med namnet df_temp_Lund.
# Kontrollera därefter att inläsningen blivit korrekt genom att
# skriva ut de första fem raderna i df_temp_Abisko och df_temp_Lund.
# Kolumnerna Datum och Tid ska i DataFrame-objekten ska konverteras
# till datetime-objekt.

# importera moduler
import pandas as pd
import matplotlib.pyplot as plt

# läs in csv-filer. Ge felmeddelande om de ej ligger i samma mapp.
fileFound = False
while not fileFound:
    try:
        df_temp_Abisko = pd.read_csv('Temperaturdata_Abisko_2019.csv', encoding='ISO-8859-1', sep=';')
        df_temp_Lund = pd.read_csv('Temperaturdata_Lund_2019.csv', encoding='ISO-8859-1', sep=';')
        fileFound = True
    except (FileNotFoundError, IOError):
        print("Placera csv-filerna i samma mapp som programfilen")
        input("Tryck på 'Retur' för att fortsätta")


# konvertera kolumnerna Datum och Tid till datetime-objekt.
df_temp_Abisko['Tid'] = pd.to_datetime(df_temp_Abisko['Tid'],format= '%H:%M:%S' ).dt.time
df_temp_Abisko['Datum'] = pd.to_datetime(df_temp_Abisko['Datum'])
df_temp_Lund['Tid'] = pd.to_datetime(df_temp_Lund['Tid'],format= '%H:%M:%S' ).dt.time
df_temp_Lund['Datum'] = pd.to_datetime(df_temp_Lund['Datum'])

# skriv ut de fem första raderna
print(df_temp_Abisko.head())
print(df_temp_Lund.head())


# deluppgift b). Skriv ett program som skapar ett DataFrame-objekt med namnet
# df_mean_values som innehåller månadsmedelvärdena (jan-dec) för temperaturerna
# i Abisko och i Lund, baserat på innehållen i df_temp_Abisko och df_temp_Lund.
# Första kolumnen i df_mean_values ska innehålla temperaturmedelvärdena från
# Abisko och andra kolumnen ska innehålla temperaturmedelvärdena från Lund.
# Använd därefter innehållet i df_mean_values för att skapa en tabell som
# presenterar månadsmedelvärdena (jan-dec).

# hämta data för varje månad och beräkna medelvärde
list_mean_Abisko = []
list_mean_Lund = []
for manad in range(1, 13):
    list_mean_Abisko.append(df_temp_Abisko[df_temp_Abisko['Datum'].dt.month == manad]['Lufttemperatur Abisko'].mean())
    list_mean_Lund.append(df_temp_Lund[df_temp_Lund['Datum'].dt.month == manad]['Lufttemperatur Lund'].mean())

# skapa dataframe df_mean_values och avrunda till en decimal
df_mean_values = pd.DataFrame(list(zip(list_mean_Abisko, list_mean_Lund)),
                              columns=['Abisko', 'Lund'])
df_mean_values = df_mean_values.round(decimals=1)

# Konstruera tabellen
print('============================================================\n')
print(f'{"" : <5}{"Månadsmedeltemperaturen i Abisko och Lund 2019": ^20}\n')
print(f'{"Månad":<10} {"":<15} {"Temperatur [C]":>5}')
print(f'{"":<20} {"Abisko":<20} {"Lund":>5}')
print('------------------------------------------------------------\n')

manader = ["jan", "feb", "mar", "apr", "maj", "jun", "jul", "aug", "sep", "okt", "nov", "dec"]
for i in range(len(manader)):
    print(f'{manader[i]:<20} {df_mean_values.iloc[i]["Abisko"]:<20} {df_mean_values.iloc[i]["Lund"]:>5}')


# deluppgift c). Använd innehållet i df_temp_Abisko och df_temp_Lund för att
# skapa ett stapeldiagram som visar högsta och lägsta temperatur per månad
# för Abisko och Lund. Diagrammen ska skapas med hjälp av programsatsen
# plt.subplot så att de två diagrammen blir placerade bredvid varandra.

# hämta maxvärde och minvärde för varje månad
list_max_Abisko = []
list_max_Lund = []
list_min_Abisko = []
list_min_Lund = []
for manad in range(1, 13):
    list_max_Abisko.append(df_temp_Abisko[df_temp_Abisko['Datum'].dt.month == manad]['Lufttemperatur Abisko'].max())
    list_max_Lund.append(df_temp_Lund[df_temp_Lund['Datum'].dt.month == manad]['Lufttemperatur Lund'].max())
    list_min_Abisko.append(df_temp_Abisko[df_temp_Abisko['Datum'].dt.month == manad]['Lufttemperatur Abisko'].min())
    list_min_Lund.append(df_temp_Lund[df_temp_Lund['Datum'].dt.month == manad]['Lufttemperatur Lund'].min())

# skapa df med min och max-värden
df_min_max_Abisko = pd.DataFrame(list(zip(manader, list_max_Abisko, list_min_Abisko)),
                              columns=['månad', 'Max temp', 'Min temp'])

df_min_max_Lund = pd.DataFrame(list(zip(manader, list_max_Lund, list_min_Lund)),
                              columns=['månad', 'Max temp', 'Min temp'])

# plotta värdena i en subplot
figure, axes = plt.subplots(1, 2, figsize=(12, 6))
df_min_max_Abisko.plot.bar(ax=axes[0], x='månad', color=['r', 'b'])
df_min_max_Lund.plot.bar(ax=axes[1], x='månad', color=['r', 'b'])

axes[0].set_title('Max- och min temperaturer i Abisko år 2019')
axes[0].set_ylabel('temperatur')
axes[1].set_title('Max- och min temperaturer i Lund år 2019')
axes[1].set_ylabel('temperatur')
plt.subplots_adjust(left=0.1,
                    bottom=0.1,
                    right=0.9,
                    top=0.9,
                    wspace=0.4,
                    hspace=0.4)
plt.show()


# deluppgift d). Använd innehållet i df_temp_Abisko och df_temp_Lund för att
# skapa en tabell enligt nedanstående utseende och som innehåller de datum då
# temperaturen i Abisko var strikt HÖGRE än i Lund.

# merge df_temp_Abisko och df_temp_Lund på datum och tid
df_temp_merged = pd.merge(df_temp_Abisko, df_temp_Lund, on=["Datum", "Tid"])

# datum till datetime-objekt och ta bort tidsangivelsen
df_temp_merged['Datum'] = pd.to_datetime(df_temp_merged['Datum'])
df_temp_merged['Datum'] = df_temp_merged['Datum'].dt.date

# hitta de datum då temp i Abisko är högre än Lund och skriv ut
for i in range(len(df_temp_merged)):
    value = df_temp_merged['Lufttemperatur Abisko'].iloc[i] > \
            df_temp_merged['Lufttemperatur Lund'].iloc[i]

# skapa tabellen
print('============================================================\n')
print(f'{"" : <0}{"Datum under 2019 då temperaturen var högre i Abisko än i Lund": ^20}\n')
print(f'{"Datum":<10} {"":<15} {"Temperatur [C]":>5}')
print(f'{"":<20} {"Abisko":>10} {"Lund":>5}')
print('------------------------------------------------------------\n')
# hitta de datum då temp i Abisko är högre än Lund och skriv ut
for i in range(len(df_temp_merged)):
    value = df_temp_merged['Lufttemperatur Abisko'].iloc[i] > \
            df_temp_merged['Lufttemperatur Lund'].iloc[i]
    if value:
        print(f'{df_temp_merged["Datum"].iloc[i]} {df_temp_merged["Lufttemperatur Abisko"].iloc[i]:>20} {df_temp_merged["Lufttemperatur Lund"].iloc[i]:>5}')

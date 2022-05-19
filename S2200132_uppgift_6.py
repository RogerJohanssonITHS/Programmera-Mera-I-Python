# -*- coding: utf-8 -*-
"""
Created on Sun May  1 13:27:58 2022

"""

# Skriv ett program som först frågar efter en kommun och därefter skapar ett
# linjediagram över medelhastigheten per vägnummer i kommunen.
# x-axeln ska vara graderad i km/h och y- axeln i tid mellan 07:00 – 18:00.
# I diagrammet ska vägnumret och högsta tillåtna hastighet finnas som etikett.
# Linjediagrammet inklusive rubriker ska ha utseende enligt nedan
# (värdena är exempelvärden).
# Medelhastigheten per timma beräknas som summan av de uppmätta hastigheterna
# under en timma dividerat med antalet fordon som passerade under samma timma.

# importera moduler
import pandas as pd
import matplotlib.pyplot as plt

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

# maska och gruppera datan på vägnummer
# inmatad kommun ger aktuella vägnummer som ger alla
# MätplatsID som skall användas
mask = (platsdata['Kommun'] == inmatadKommun)

# hitta aktuella MätplatsID och data
matPlatser = platsdata[mask].groupby(['Vägnummer'])

# konvertera kolumnen Tid till ett datetime-objekt
kameradata['Tid'] = pd.to_datetime(kameradata['Tid'])

# skapa variabler för att hålla summan av hastigheterna vid en mätplats
# och antalet fordon som passerat
matplatsSummaHastigheter = 0
matplatsAntalFordon = 0
vagSummaHastigheter = []
vagAntalFordon = []

# skapa variabel för att spara de etiketter som skall användas i grafen
# (vägnummer, gällande hastighet) i en tuple
maxHastLabelPlot = []

# loopa igenom mätplatserna för varje kommun
for key in matPlatser.groups.keys():
    matplatsID = matPlatser.get_group(key)['MätplatsID'].tolist()

    for i in matplatsID:
        maxHastLabelPlot.append((platsdata[platsdata['MätplatsID'] == i]
            ['Vägnummer'].values[0], kameradata[kameradata['MätplatsID'] == i]['Gällande Hastighet'].max()))

    # loopa mätplatsID över de aktuella timmarna och summera de
    # uppmätta hastighetrna och antal fordon
    vagsumma = []
    vagfordon = []
    for timma in range(7, 18):
        for i in matplatsID:
            mask = (kameradata['Tid'].dt.hour >= timma) & (kameradata['Tid'].dt.hour < timma + 1)
            matplatsSummaHastigheter += kameradata[mask][kameradata['MätplatsID'] == i]['Hastighet'].sum()
            matplatsAntalFordon += kameradata[mask][kameradata['MätplatsID'] == i]['Hastighet'].count()
        # när alla mätplatser för vägen är summerade; spara resultatet timvis
        vagsumma.append(matplatsSummaHastigheter)
        vagfordon.append(matplatsAntalFordon)
        # nollställ variablerna
        matplatsSummaHastigheter = 0
        matplatsAntalFordon = 0
    # lägg till listan till slutlistan
    vagSummaHastigheter.append(vagsumma)
    vagAntalFordon.append(vagfordon)

# ordna med genitiv-s på kommunnamnet och lägg till kommun
if inmatadKommun[-1] != "s":
    inmatadKommunGenitiv = inmatadKommun + "s" + " kommun"
else:
    inmatadKommunGenitiv = inmatadKommun + " kommun"

# Skapa ett linjediagram och beräkna medelhastigheterna för varje väg
klockslagEtiketter = ['8:00', '9:00', '10:00','11:00', '12:00', '13:00', '14:00','15:00', '16:00', '17:00', '18:00']
plt.xticks(rotation=45)
plt.grid()
plt.xlabel('Klockslag')
plt.ylabel('Medelhasighet (km/h)')
titelGraf = "Medelhastigheter uppmätta per vägnummer i " + inmatadKommunGenitiv + " under perioden 2021-09-11 kl. 07.00 - 18.00"
plt.title(titelGraf)

# gör om listan med tuples till dataframe för gruppering
labels = pd.DataFrame(maxHastLabelPlot, columns = ['Vägnummer', 'Maxhastighet'])
labelsKomprimerad = labels.groupby(['Vägnummer'])['Maxhastighet'].max()
lazyListaLabels = []
for a in labelsKomprimerad.items():
    lazyListaLabels.append(a)

# skapa variabel för att spara medelhastigheterna per timma
medelHastighetPerTimma = []
for count, summaHast in enumerate(zip(vagSummaHastigheter, vagAntalFordon)):
    labelText = "Väg " + lazyListaLabels[count][0] + " - " + str(int(lazyListaLabels[count][1])) +" km/h"
    for i in range(len(summaHast[0])):
        medelHastighetPerTimma.append(round(summaHast[0][i]/summaHast[1][i],1))
    plt.plot(klockslagEtiketter, medelHastighetPerTimma, label=labelText)
    medelHastighetPerTimma.clear()

plt.legend(loc="lower left")
plt.show()
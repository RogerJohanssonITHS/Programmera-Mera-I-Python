# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 22:46:00 2022

"""

# importera moduler
import pandas as pd

# läs in csv-fil
pafoljd = pd.read_csv('pafoljd.csv', encoding='ISO-8859-1', sep=';')


print(type(pafoljd))
print(pafoljd)
granser = pafoljd['Hastighetsöverträdelse (km/h)'].squeeze()
straff = pafoljd['Påföljd'].squeeze()
print(type(granser))
print(granser)
print(type(straff))
print(straff)

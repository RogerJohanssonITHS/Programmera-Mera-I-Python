# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 09:42:40 2022

"""

# importera moduler
import pandas as pd
import numpy as np

# läs in csv-fil
pafoljd = pd.read_csv('pafoljd.csv', encoding='ISO-8859-1', sep=';')

# gör om pafoljd till panda.Series
granser = pafoljd['Hastighetsöverträdelse (km/h)'].squeeze()
straffSatser = pafoljd['Påföljd'].squeeze()
print(type(granser))
print(granser)
print(type(straffSatser))
print(straffSatser)
idx = np.argmax(granser >= 70)
print(idx)
print(straffSatser[idx])

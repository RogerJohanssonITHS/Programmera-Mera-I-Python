# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 18:00:59 2022

"""

# importera moduler
import pandas as pd
import matplotlib as plt

# läs in csv-filer
kameradata = pd.read_csv('kameraData.csv', encoding='ISO-8859-1', sep=';')
pafoljd = pd.read_csv('pafoljd.csv', encoding='ISO-8859-1', sep=';')
platsdata = pd.read_csv('platsData.csv', encoding='ISO-8859-1', sep=';')

# Skapa ett program som beräknar summan av antal fordon som kamerorna har
# registrerat över alla mätplatser uppdelat per timma mellan kl. 07:00 och 18:00.

# använd kameradata
# hur väljer man ut rader mellan klockslag?

# Skapa därefter ett linjediagram över resultatet där x-axeln är graderad
# i timmar mellan 07.00 och 18.00 och y-axeln i antal registrerade fordon.

# Rubrik: Totalt antal fordon som kamerorna registrerar i mätområdet 2021-09-11
# Y-axel: Antal fordon
# X-axel: Klockslag
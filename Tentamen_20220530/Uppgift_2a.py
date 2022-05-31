# -*- coding: utf-8 -*-
"""
Created on Wed May 25 13:20:00 2022

@author: S2200132
"""

# En godtycklig triangel kan klassificeras utifrån längden på
# dess sidor och kan antingen vara liksidig, likbent eller oliksidig.

# 1. En liksidig triangel är en triangel med tre lika sidor
# 2. En likbent triangel är en triangel som har två lika sidor
# 3. En oliksidig triangel är en triangel där inga sidor är lika

# Din uppgift blir att först skapa en Python-klass med namnet Triangel som
# klassificerar en godtycklig triangel och därefter beräknar arean av denna.
# Skapa därefter ett huvudprogram som frågar efter en triangels
# sidor (a, b och c) och som därefter undersöker vilken typ av triangel det är
# och skriver ut resultatet på skärmen tillsammans med arean av triangeln genom
# att anropa klassen Triangel.
# Variablerna som ingår i klassen Triangel behöver inte vara privata.

# importera moduler
import numpy as np


# klassen Triangel
class Triangel:
    def __init__(self, a=0, b=0, c=0, klassificering=""):
        self.a = a
        self.b = b
        self.c = c
        self.set_klassificering()

    def area(self):
        s = (a+b+c)/2
        return np.sqrt(s*(s-a)*(s-b)*(s-c))

    def set_klassificering(self):
        listaKlasser = ["liksidig", "likbent", "oliksidig"]
        # kontrollera om triangeln är likbent
        if (self.a == self.b) and (self.a != self.c):
            self.klassificering = listaKlasser[1]
            return
        # kontrollera om triangeln är liksidig
        if (self.a == self.b) and (self.a == self.c):
            self.klassificering = listaKlasser[0]
            return
        # triangeln är oliksidig
        self.klassificering = listaKlasser[2]
        return

    def get_klassificering(self):
        return self.klassificering


# klassen LiksidigTriangel
class LiksidigTriangel(Triangel):
    def __init__(self, a=0, klassificering=""):
        super().__init__(a=a, b=a, c=a, klassificering="")

    def area(self):
        return np.sqrt(3)*pow(self.a, 2)/4


# huvudprogram
a = float(input("Ange längden på sida 1: "))
b = float(input("Ange längden på sida 2: "))
c = float(input("Ange längden på sida 3: "))

skapadTriangel = Triangel(a, b, c)
print(f'Det är en {skapadTriangel.get_klassificering()} triangel \nArean = {skapadTriangel.area():.2f}')

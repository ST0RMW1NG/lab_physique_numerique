# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 13:05:00 2023

@author: teemo
"""

x=4.965
x=float(x)
c=3*10**8
k=1.380649*10**-23
h=6.62607015*10**-34
b=(((h*c)/(x*k))*1000000000)
tsoleil=5780
torion=3590
tsirius=9940

print("La longueur d'onde max pour le soleil est",int((b/tsoleil)),'nm')
print("La longueur d'onde max pour Sirius est",int((b/tsirius)),'nm')
print("La longueur d'onde max pour Bételgeuse est",int((b/torion)),'nm')
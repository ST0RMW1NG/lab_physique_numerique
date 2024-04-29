# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 12:29:04 2023

@author: teemo
"""

from math import exp
a=input("Veuillez choisir une valeur de a")
a=float(a)
e=input("Veuillez choisir une valeur de la marge d'erreur")
e=float(e)
x=a
x=float(x) 
z=x-(a*(1-exp(-x))) #on défini z comme étant la valeur du calcul de l'erreur
x=a*(1-exp(-x))
y=1
y=int(y)


while(e<z):    
    z=x-(a*(1-exp(-x)))
    x=a*(1-exp(-x))
    print('Itération numero',y)
    print('La valeur actuelle de x est',x)
    print('La valeur de la marge d\'erreur est',z)
    y+=1
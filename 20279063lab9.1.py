# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 16:17:54 2023

@author: teemo
"""

import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng()

n_m = 1000  # nombre de marcheurs??
n_pas = 1001  # nombre de pas (+1 car le pas 0 est la position initiale)
x = np.zeros((n_m, n_pas))  # position en x de chaque marcheur à chaque pas, initialement à 0
y = np.zeros((n_m, n_pas))  # position en y de chaque marcheur à chaque pas, initialement à 0

for k in range(1, n_pas):  # boucle sur les pas
    theta = rng.random(n_m) * 2 * np.pi  # choix de la direction
    x[:, k] = x[:, k - 1] + np.cos(theta)  # déplacement en x
    y[:, k] = y[:, k - 1] + np.sin(theta)  # déplacement en y

# Positions aux pas 10, 30, 100, 300, 1000
pas_indices = [1000, 300, 100, 30, 10]

# Couleurs pour chaque pas
colors = ['blue', 'orange', 'green', 'red', 'purple']

# Affichage des positions
for pas_index, color in zip(pas_indices, colors):
    plt.scatter(x[:, pas_index], y[:, pas_index], s=5, c=color, label=f'Pas {pas_index}')


#graph des positions au pas 10,30,100,300,1000
plt.axhline(ls=':')
plt.axvline(ls=':')
plt.xlabel('Position x')
plt.ylabel('Position y')
plt.axis('equal')
plt.legend()
plt.savefig('fractalq1.png')
plt.show()

#graph du deplacement quad moyen
d_quad= x**2+y**2
dQuadMoy=(x**2+y**2).mean(axis=0)
plt.plot(dQuadMoy)
plt.plot(np.arange(n_pas+1))
plt.xlabel('Itération (# du pas)')
plt.ylabel('Déplacement quadratique moyen')
plt.savefig('deplacementquadmoyq1.png')
print('deplacement quadratique moyen', dQuadMoy)
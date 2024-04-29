# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 16:17:54 2023

@author: teemo
"""

import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng()

def simulation_agregation(N, M, n_iter_max=200000):
    
    #N: taille du réseau
    #M: nombre de marcheurs
    #n_iter_max: nombre maximal d'itérations temporelles
    
    #positions initiales des marcheurs
    x = rng.integers(1, N, M, endpoint=True)
    y = rng.integers(1, N, M, endpoint=True)
    
    status_mobile = np.ones(M, dtype='bool')  #true poiur un marcheur mobile
    grille_fixe = np.zeros([N+2, N+2], dtype='bool') #tru pour un marcheur fixe
    
    grille_fixe[:, 0] = True
    
    n_fixe = 0 #nombre de marcheurs fixe
    n_iter = 0 #nombre d'iteration
    
    while (n_fixe < M) and (n_iter < n_iter_max):
        m, = status_mobile.nonzero()
        
        directions = rng.choice([0, 1, 2, 3], size=m.size) #choix aleatoire de la direction
        
        x[m] = np.clip(x[m] + np.where(directions == 0, 1, np.where(directions == 1, -1, 0)), 1, N)
        y[m] = np.clip(y[m] + np.where(directions == 2, 1, np.where(directions == 3, -1, 0)), 1, N)
        
        voisin_fixe = grille_fixe[x[m] - 1, y[m] - 1] + \
                      grille_fixe[x[m], y[m] - 1] + \
                      grille_fixe[x[m] + 1, y[m] - 1] + \
                      grille_fixe[x[m] + 1, y[m]] + \
                      grille_fixe[x[m] + 1, y[m] + 1] + \
                      grille_fixe[x[m], y[m] + 1] + \
                      grille_fixe[x[m] - 1, y[m] + 1] + \
                      grille_fixe[x[m] - 1, y[m]]
        
        k = m[voisin_fixe.nonzero()[0]] #tableau des indices des marcheurs qui se fixent a un voisin
        
        if k.size > 0: #est-ce que le marcheur est fixe
            status_mobile[k] = False
            grille_fixe[x[k], y[k]] = True
            n_fixe += k.size
        
        n_iter += 1
    
    return x, y, grille_fixe[1:N+1, 1:N+1]

# Exemple d'utilisation
N = 256
M = 5000
grille_fixe_final = simulation_agregation(N, M)

# Visualisation de la fractale
plt.imshow(grille_fixe_final[2].T, origin='lower', cmap='binary')
plt.title('Fractale résultante')
plt.savefig('fractalq2.png')
plt.show()
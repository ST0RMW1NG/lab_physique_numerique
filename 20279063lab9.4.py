# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 16:18:01 2023

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
    
    status_mobile = np.ones(M, dtype='bool')
    grille_fixe = np.zeros([N+2, N+2], dtype='bool')
    
    grille_fixe[:, 0] = True
    
    n_fixe = 0 #nombre de marcheur fixe initial
    n_iter = 0 #nombre d'iteration
    
    nombre_marcheurs_fixes = []  # Nouvelle liste pour stocker le nombre de marcheurs fixes à chaque itération
    
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
        nombre_marcheurs_fixes.append(n_fixe)  # Ajout du nombre de marcheurs fixes à chaque itération
    
    return x, y, grille_fixe[1:N+1, 1:N+1], nombre_marcheurs_fixes

#valeur N et M
Nvaleurs=[128,256,512,1048]
N = Nvaleurs
M_values = [5000, 5000, 5000, 5000]

 #graph des fractale
for N,M in zip(Nvaleurs, M_values):   
    x_final, y_final, grille_fixe_final, _ = simulation_agregation(N, M)
    plt.imshow(grille_fixe_final.T, origin='lower', cmap='binary', label=f'M = {M}')
    plt.title('Fractale résultante' f'N = {N}')
    plt.savefig(f'N = {N}.png')
    plt.show()

# gaph de la croissance de l'agrégat
for N in Nvaleurs:
    _, _, _, nombre_marcheurs_fixes = simulation_agregation(N, M)
    
    plt.plot(nombre_marcheurs_fixes, label=f'M = {M}')
    plt.xlabel('Itération temporelle')
    plt.ylabel('Nombre de marcheurs fixes')
    plt.title(f'N = {N}')
    plt.legend()
    plt.savefig('courbecroi'f'N = {N}.png')
    plt.show()
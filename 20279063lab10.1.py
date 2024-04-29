# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 23:41:07 2023

@author: teemo
"""

import numpy as np
import matplotlib.pyplot as plt

N = 128  # taille du réseau
M = 5000  # nombre de marcheurs
L = 20  # durée de survie des malades
n_iter_max = 5000  # nombre maximal d'itérations temporelles

simulations = range(1, 13)
for sim in simulations:
    rng = np.random.default_rng()  # initialisation du générateur aléatoire
    
    x = rng.integers(0, N, M)  # positions initiales des marcheurs
    y = rng.integers(0, N, M)  # positions initiales des marcheurs
    infecte = np.zeros(M, dtype='int')  # statut (0: santé, 1: infecté, 2: mort)
    survie = np.zeros(M, dtype='int')  # temps de survie restant, si infecté
    
    jj = rng.integers(0, M)  # sélection au hasard d'un marcheur
    infecte[jj] = 1  # infection de ce marcheur
    survie[jj] = L  # temps de survie restant de ce marcheur
    n_infecte = 1  # le nombre total de marcheurs infectés
    n_mort = 0  # le nombre total de marcheurs morts
    n_iter = 0
    
    # Listes pour stocker les données pour le tracé
    infectes_au_fil_du_temps = [n_infecte]
    en_vie_au_fil_du_temps = [M - n_mort]  # Nombre initial de marcheurs en vie
    iterations = [n_iter]
    
    while (n_infecte > 0) and (n_iter < n_iter_max):  # itération temporelle
        v, = (infecte < 2).nonzero()  # indices des marcheurs vivants
    
        # Mouvement des marcheurs
        pas_x = rng.integers(-1, 2, size=len(v))
        pas_y = rng.integers(-1, 2, size=len(v))
        x[v] = np.clip(x[v] + pas_x, 0, N - 1)
        y[v] = np.clip(y[v] + pas_y, 0, N - 1)
    
        # Contagion
        for j in (infecte == 1).nonzero()[0]:
            k, = ((x == x[j]) & (y == y[j]) & (infecte == 0)).nonzero()
    
            if k.size > 0:
                infecte[k] = 1
                survie[k] = L
                n_infecte += len(k)
    
        # Gestion de la mort
        for j in (infecte == 1).nonzero()[0]:
            survie[j] -= 1
    
            if survie[j] == 0:
                infecte[j] = 2
                n_infecte -= 1
                n_mort += 1
        
        # Ajouter des données pour le tracé
        iterations.append(n_iter)
        infectes_au_fil_du_temps.append(n_infecte)
        en_vie_au_fil_du_temps.append(M - n_mort)
    
        # Visualisation de la simulation
        if n_iter % 100 == 0:  
            plt.figure(figsize=(8, 6))
            plt.scatter(x, y, c=infecte, cmap='jet', s=8)
            plt.title(f'Simulation {sim}, Itération {n_iter}: {n_infecte} Infectés, {M - n_mort} En vie')
            plt.colorbar(label='État de santé')
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.savefig(f'Simulation {sim}, Itération {n_iter}.png')
            plt.show()
            print('Simulation #', sim, "Itération {}: {} malades, {} morts.".format(n_iter, n_infecte, n_mort))
        
        n_iter += 1

    # Tracer le nombre d'infectés et de marcheurs en vie au fil du temps après la simulation
    plt.figure(figsize=(8, 6))
    plt.plot(iterations, infectes_au_fil_du_temps, label='Infectés')
    plt.xlabel('Itération')
    plt.ylabel('Nombre de marcheurs infectés')
    plt.title(f'Simulation {sim}')
    plt.twinx()
    plt.plot(iterations, en_vie_au_fil_du_temps, color='green')
    plt.ylabel('Nombre de marcheurs en vie')
    plt.savefig(f'Simulation {sim}.png')
    plt.show()

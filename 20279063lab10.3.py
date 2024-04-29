# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 23:37:50 2023

@author: teemo
"""

import numpy as np
import matplotlib.pyplot as plt

def simuler_epidemie_vaccination(N, M, L, n_iter_max, taux_vaccination, num_simulations):
    rng = np.random.default_rng()  # initialise le générateur de nombres aléatoires

    # Initialisation des positions des marcheurs
    x = rng.integers(0, N, M)
    y = rng.integers(0, N, M)

    infecte = np.zeros(M, dtype='int')  # statut (0: sain, 1: infecté, 2: mort)
    survie = np.zeros(M, dtype='int')  # temps de survie restant, s'ils sont infectés

    # Sélectionner de manière aléatoire un pourcentage de marcheurs à vacciner
    num_vaccines = int(M * taux_vaccination)
    marcheurs_vaccines = rng.choice(M, num_vaccines, replace=False)
    prob_vaccination = np.ones(M)
    prob_vaccination[marcheurs_vaccines] = 0.05  # probabilité d'infection de 5 % pour les marcheurs vaccinés

    jj = rng.integers(0, M)  # sélectionner de manière aléatoire un marcheur infecté initial
    infecte[jj] = 1
    survie[jj] = L
    n_infecte = 1  # nombre total de marcheurs infectés
    n_morts = 0  # nombre total de marcheurs morts
    n_iter = 0

    # Listes pour stocker les données pour le tracé
    infectes_au_fil_du_temps = [n_infecte]
    en_vie_au_fil_du_temps = [M - n_morts]  # Nombre initial de marcheurs en vie
    iterations = [n_iter]

    while (n_infecte > 0) and (n_iter < n_iter_max):  # itération temporelle
        v, = (infecte < 2).nonzero()  # indices des marcheurs vivants

        # Mouvement des marcheurs
        pas_x = rng.integers(-1, 2, size=len(v))
        pas_y = rng.integers(-1, 2, size=len(v))
        x[v] = np.clip(x[v] + pas_x, 0, N - 1)
        y[v] = np.clip(y[v] + pas_y, 0, N - 1)

        # Infection
        for j in (infecte == 1).nonzero()[0]:
            k, = ((x == x[j]) & (y == y[j]) & (infecte == 0)).nonzero()

            if k.size > 0:
                # Test probabiliste pour déterminer quels marcheurs seront infectés
                prob_infection = rng.uniform(size=len(k))
                infectes_k = k[prob_infection < prob_vaccination[j]]

                infecte[infectes_k] = 1
                survie[infectes_k] = L
                n_infecte += len(infectes_k)

        # Gestion de la mort
        for j in (infecte == 1).nonzero()[0]:
            survie[j] -= 1

            if survie[j] == 0:
                infecte[j] = 2
                n_infecte -= 1
                n_morts += 1

        # Ajouter des données pour le tracé
        iterations.append(n_iter)
        infectes_au_fil_du_temps.append(n_infecte)
        en_vie_au_fil_du_temps.append(M - n_morts)
        # Visualisation de la simulation
        if n_iter % 100 == 0:  
            plt.figure(figsize=(8, 6))
            plt.scatter(x, y, c=infecte, cmap='jet', s=8)
            plt.title(f'Simulation {sim}, Itération {n_iter}: {n_infecte} Infectés, {M - n_morts} En vie')
            plt.colorbar(label='État de santé')
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.savefig(f'Simulationsq3 {sim}, Itération {n_iter}.png')
            plt.show()
            print('Simulation #', sim, "Itération {}: {} malades, {} morts.".format(n_iter, n_infecte, n_morts))

        n_iter += 1

    # Tracer le nombre d'infectés et de marcheurs en vie au fil du temps 
    plt.figure(figsize=(8, 6))
    plt.plot(iterations, infectes_au_fil_du_temps, label='Infectés')
    plt.xlabel('Itération')
    plt.ylabel('Nombre de marcheurs infectés')
    plt.title('Simulation d\'épidémie')
    plt.twinx()
    plt.plot(iterations, en_vie_au_fil_du_temps, color='green')
    plt.ylabel('Nombre de marcheurs en vie')
    plt.savefig(f'Simulations d\'épidémie {sim}.png')
    plt.show()

    # Retourner le taux de mortalité final et la durée de l'épidémie
    taux_mortalite = n_morts / M
    duree_epidemie = n_iter

    return taux_mortalite, duree_epidemie


# Paramètres
M = 5000
L = 20
n_iter_max = 5000
taux_vaccination = 0.75
num_simulations = 12
densite = 0.5

# Listes pour stocker les résultats de chaque simulation
taux_mortalite = []
durees_epidemie = []

# Exécuter plusieurs simulations
for sim in range(num_simulations):
    N = int(np.sqrt(M / densite))
    taux_mort, duree_epidemie = simuler_epidemie_vaccination(N, M, L, n_iter_max, taux_vaccination, num_simulations)
    taux_mortalite.append(taux_mort)
    durees_epidemie.append(duree_epidemie)

# Calculer le taux moyen de mortalité et la durée moyenne de l'épidémie à travers les simulations
taux_mortalite_moyen = np.mean(taux_mortalite)
duree_epidemie_moyenne = np.mean(durees_epidemie)

print(f'Taux moyen de mortalité : {taux_mortalite_moyen}')
print(f'Durée moyenne de l\'épidémie : {duree_epidemie_moyenne}')

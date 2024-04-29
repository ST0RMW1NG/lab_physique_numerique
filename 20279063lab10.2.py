# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 23:41:07 2023

@author: teemo
"""

import numpy as np
import matplotlib.pyplot as plt

def simuler_epidemie(N, M, L, n_iter_max, num_simulations):
    taux_mortalite = []
    durees_epidemie = []
    rng = np.random.default_rng()  # initialise le générateur de nombres aléatoires

    x = rng.integers(0, N, M)  # positions initiales des marcheurs
    y = rng.integers(0, N, M)  # positions initiales des marcheurs
    infecte = np.zeros(M, dtype='int')  # statut (0: sain, 1: infecté, 2: mort)
    survie = np.zeros(M, dtype='int')  # temps de survie restant si infecté

    jj = rng.integers(0, M)  # sélectionner de manière aléatoire un marcheur
    infecte[jj] = 1  # infecter ce marcheur
    survie[jj] = L  # temps de survie restant de ce marcheur
    n_infecte = 1  # nombre total de marcheurs infectés
    n_mort = 0  # nombre total de marcheurs morts
    n_iter = 0

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

        n_iter += 1

    # Ajouter le taux de mortalité et la durée de l'épidémie pour chaque simulation
    taux_mortalite_simulation = n_mort / M
    taux_mortalite.append(taux_mortalite_simulation)
    durees_epidemie.append(n_iter)

    # Calculer le taux moyen de mortalité et la durée moyenne de l'épidémie
    taux_mortalite_moyen = np.mean(taux_mortalite)
    duree_epidemie_moyenne = np.mean(durees_epidemie)

    return taux_mortalite_moyen, duree_epidemie_moyenne

# Paramètres
M = 5000
L = 20
n_iter_max = 5000
num_simulations = 12

# Valeurs de densité
valeurs_densite = np.arange(0.15, 0.55, 0.05)

# Tableaux pour stocker les résultats
μ_tableau = np.zeros((len(valeurs_densite), num_simulations))
T_tableau = np.zeros((len(valeurs_densite), num_simulations))

# Itérer sur les valeurs de densité
for i, densite in enumerate(valeurs_densite):
    N = int(np.sqrt(M / densite))
    
    # Listes pour stocker les résultats de chaque simulation
    taux_mortalite_simulations = []
    durees_epidemie_simulations = []
    
    # Exécuter plusieurs simulations pour chaque valeur de densité
    for j in range(num_simulations):
        taux_mortalite_moyen, duree_epidemie_moyenne = simuler_epidemie(N, M, L, n_iter_max, num_simulations)
        taux_mortalite_simulations.append(taux_mortalite_moyen)
        durees_epidemie_simulations.append(duree_epidemie_moyenne)
        
        # Stocker les résultats dans les tableaux
        μ_tableau[i, j] = taux_mortalite_moyen
        T_tableau[i, j] = duree_epidemie_moyenne

# Calculer la moyenne et l'écart type à travers les simulations pour chaque valeur de densité
μ_moyen = np.mean(μ_tableau, axis=1)
T_moyen = np.mean(T_tableau, axis=1)
μ_ecart_type = np.std(μ_tableau, axis=1)
T_ecart_type = np.std(T_tableau, axis=1)

# Tracer le taux moyen de mortalité par rapport à la densité avec des barres d'erreur
plt.errorbar(valeurs_densite, μ_moyen, yerr=μ_ecart_type, fmt='o-', label='Taux moyen de mortalité')
plt.xlabel('Densité (ρ)')
plt.ylabel('Taux moyen de mortalité')
plt.title('Taux moyen de mortalité par rapport à la densité')
plt.legend()
plt.grid()
plt.savefig('Taux moyen de mortalité par rapport à la densité.png')
plt.show()

# Tracer la durée moyenne de l'épidémie par rapport à la densité avec des barres d'erreur
plt.errorbar(valeurs_densite, T_moyen, yerr=T_ecart_type, fmt='o-', label='Durée moyenne de l\'épidémie')
plt.xlabel('Densité (ρ)')
plt.ylabel('Durée moyenne de l\'épidémie')
plt.title('Durée moyenne de l\'épidémie par rapport à la densité')
plt.legend()
plt.grid()
plt.savefig('Durée moyenne de l\'épidémie par rapport à la densité.png')
plt.show()


# Tracer les résultats
for j in range(num_simulations):
    plt.scatter(μ_tableau[:, j], T_tableau[:, j], label=f'Simulation {j + 1}')
plt.xlabel('Taux moyen de mortalité (μ)')
plt.ylabel('Durée moyenne de l\'épidémie (T)')
plt.title('μ vs. T pour différentes simulations et valeurs de densité')
plt.legend()
plt.grid()
plt.savefig('μ vs. T pour différentes simulations et valeurs de densité.png')
plt.show()

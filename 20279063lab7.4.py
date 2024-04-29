# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 19:54:39 2023

@author: teemo
"""

import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt



# Chargez  le fichier
t, x, sigx, y, sigy = np.loadtxt('mesuresOrbite2023.txt', unpack=True)
m_etoile=1.15

def calc_anom_exc(M, e, epsilon=1.e-10, iterMax=25):
    # Initial guess based on the condition
    E = np.where((M % (2 * np.pi)) < np.pi, M + e / 2, M - e / 2)

    # Newton
    for _ in range(iterMax):
        f = E - e * np.sin(E) - M
        df = 1 - e * np.cos(E)
        E = E - f / df

        # Convergence
        if np.all(np.abs(f) < epsilon):
            break

    return E

def calc_orbite(p, t, m_etoile):
    a, e, M0, Omega, inclination, omega = p
    t = np.atleast_1d(t)

    # Calcul de la période orbitale
    P = np.sqrt(a**3 / m_etoile)

    # Calcul de l'anomalie moyenne
    M = 2 * np.pi * t / P + M0

    # Calcul de l'anomalie excentrique
    E = calc_anom_exc(M, e)

    # Calcul des coordonnées polaires r et θ
    r = a * (1 - e * np.cos(E))
    theta = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2), np.sqrt(1 - e) * np.cos(E / 2))

    # Transformation vers le référentiel désiré (x, y)
    xprime = r * np.cos(theta)
    yprime = r * np.sin(theta)

    # Transformation des coordonnées vers le plan duz ciel
    x = (np.cos(omega) * np.cos(Omega) - np.cos(inclination) * np.sin(Omega) * np.sin(omega)) * xprime - \
        (np.sin(omega) * np.cos(Omega) + np.cos(inclination) * np.sin(Omega) * np.cos(omega)) * yprime

    y = (np.cos(omega) * np.sin(Omega) + np.cos(inclination) * np.cos(Omega) * np.sin(omega)) * xprime - \
        (np.sin(omega) * np.sin(Omega) - np.cos(inclination) * np.cos(Omega) * np.cos(omega)) * yprime

    return x, y
#la fonction de X²
def chi2_orb(p, t, x, sigx, y, sigy):
    m_etoile=1.15
    xm, ym = calc_orbite(p, t, m_etoile)
    chi2 = np.sum(((x - xm) / sigx) ** 2 + ((y - ym) / sigy) ** 2)
    return chi2

#les bornes pour chaque paramètre
bornes = ((0, None), (0, 1), (0, 2 * np.pi), (0, 2 * np.pi), (0, np.pi), (0, 2 * np.pi))

#la minimisation avec différents points de départ
nombre_repetitions = 10
resultats_minimisation = []

for _ in range(nombre_repetitions):
    #estimés initiaux aléatoires
    p0_initial_guess = np.random.rand(6)

    #la minimisation
    resultats = minimize(chi2_orb, p0_initial_guess, args=(t, x, sigx, y, sigy),
                         method='SLSQP', bounds=bornes)

    # Ajout du résultat à la liste
    resultats_minimisation.append(resultats)

#le meilleur ajustement (minimum global)
meilleur_resultat = min(resultats_minimisation, key=lambda x: x.fun)

#le résultat
print("Meilleur résultat de la minimisation :")
print("Paramètres optimisés :", meilleur_resultat.x)
print("Valeur minimale de X² :", meilleur_resultat.fun)

#l'orbite avec les paramètres optimisés
time_range = np.linspace(0, 50, 1000)
x_opt, y_opt = calc_orbite(meilleur_resultat.x, time_range, m_etoile)

plt.figure(figsize=(8, 8))
plt.axhline(0, color='black', linestyle='--')
plt.axvline(0, color='black', linestyle='--')
plt.axis('equal')
plt.errorbar(x, y, xerr=sigx, yerr=sigy, linestyle='', marker='o', label='Mesures')
plt.plot(x_opt, y_opt, label='Orbite ajustée')
plt.title('Ajustement de l\'orbite aux mesures')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.savefig('ajustementdelorbite.png')
plt.show()

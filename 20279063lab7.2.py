# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 19:54:33 2023

@author: teemo
"""

import numpy as np
import matplotlib.pyplot as plt

def calc_anom_exc(M, e, epsilon=1.e-10, iterMax=25):
    # Initial guess
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
    a, e, M0 = p
    t = np.atleast_1d(t)

    # Calcul de la période orbitale
    P = np.sqrt(a**3 / m_etoile)

    # Calcul de l'anomalie moyenne
    M = (2 * np.pi * t / P) + M0

    # Calcul de l'anomalie excentrique 
    E = np.zeros_like(M)
    for i in range(len(M)):
        E[i] = calc_anom_exc(M[i], e)

    # Calcul des coordonnées polaires r et theta
    r = a * (1 - e * np.cos(E))
    theta = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2), np.sqrt(1 - e) * np.cos(E / 2))

    # Conversion des coordonnées polaires en coordonnées cartésiennes
    xprime = r * np.cos(theta)
    yprime = r * np.sin(theta)

    return xprime, yprime

# Paramètres pour les trois figures
m_etoile = 1.0

# Fig 1

plt.figure(figsize=(8, 8))
for e_value in [0.0, 0.5, 0.8]:
    params_fig1 = [1.0, 0.0, 0.0]  
    params_fig1[1] = e_value
    xprime, yprime = calc_orbite(params_fig1, np.linspace(0, 1, 1000), m_etoile)
    plt.plot(xprime, yprime, label=f"e={e_value}")
    plt.scatter(xprime[::100], yprime[::100], color='red')  # Points rouges aux sauts de 0.1 an
plt.axhline(0, color='black', linestyle='--')
plt.axvline(0, color='black', linestyle='--')
plt.xlabel("x'")
plt.ylabel("y'")
plt.title("Orbites pour différentes valeurs de e")
plt.legend()
plt.axis('equal')
plt.savefig('orbitespourdiffvaldee.png')
plt.show()

plt.figure(figsize=(8, 8))
for M0_value in [0, np.pi/2, np.pi]:
    params_fig2 = [3.0, 0.5, 0.0]
    params_fig2[2] = M0_value
    xprime, yprime = calc_orbite(params_fig2, np.linspace(0, 1, 1000), m_etoile)
    plt.plot(xprime, yprime, label=f"M0={M0_value}")
    plt.scatter(xprime[::100], yprime[::100], color='red')  # Points rouges aux sauts de 0.1 an
plt.axhline(0, color='black', linestyle='--')
plt.axvline(0, color='black', linestyle='--')
plt.xlabel("x'")
plt.ylabel("y'")
plt.title("Orbites pour différentes valeurs de M0 ")
plt.legend()
plt.axis('equal')
plt.savefig('orbitespourdiffvaldeM0.png')
plt.show()

plt.figure(figsize=(8, 8))
for m_etoile_value in [1.0, 0.25]:
    params_fig3 = [1.0, 0.5, 0.0]  
    params_fig3[0] = m_etoile_value
    xprime, yprime = calc_orbite(params_fig3, np.linspace(0, 1, 1000), m_etoile_value)
    plt.plot(xprime, yprime, label=f"M⋆={m_etoile_value} M⊙")
    plt.scatter(xprime[::100], yprime[::100], color='red')  # Points rouges aux sauts de 0.1 an
plt.axhline(0, color='black', linestyle='--')
plt.axvline(0, color='black', linestyle='--')
plt.xlabel("x'")
plt.ylabel("y'")
plt.title("Orbites pour différentes valeurs de M⋆ ")
plt.legend()
plt.axis('equal')
plt.savefig('orbitepourdiffvaleurdeM⋆.png')
plt.show()
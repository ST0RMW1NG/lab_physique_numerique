# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 19:54:36 2023

@author: teemo
"""

import numpy as np
import matplotlib.pyplot as plt

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

params_circle = [1.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # Cercle
params_straight_line = [1.0, 0.0, 0.0, 0.0, np.pi / 2, 0.0]  # Ligne droite
params_inclination = [1.0, 0.2, 0.0, 0.0, np.pi / 4, 0.0]  # Effet de l'inclinaison
params_excentricity = [1.0, 0.5, 0.0, 0.0, 0.0, 0.0]  # Effet de l'excentricité
params_rotation = [1.0, 0.2, 0.0, np.pi / 4, np.pi / 4, np.pi / 6]  # Vérification des angles Ω, i, et ω

# Générer des orbites
time_range = np.linspace(0, 1, 1000)
orbit_circle = calc_orbite(params_circle, time_range, 1.0)
orbit_straight_line = calc_orbite(params_straight_line, time_range, 1.0)
orbit_inclination = calc_orbite(params_inclination, time_range, 1.0)
orbit_excentricity = calc_orbite(params_excentricity, time_range, 1.0)
orbit_rotation = calc_orbite(params_rotation, time_range, 1.0)

# figure des orbites
plt.figure(figsize=(12, 12))

plt.subplot(3, 2, 1)
plt.axhline(0, color='black', linestyle='--')
plt.axvline(0, color='black', linestyle='--')
plt.plot(orbit_circle[0], orbit_circle[0])
plt.scatter(orbit_circle[0][::100], orbit_circle[0][::100], color='red')  # Points rouges aux sauts de 0.1 an
plt.title('Cercle (e = 0, i = 0)')
plt.axis('equal')

plt.subplot(3, 2, 2)
plt.axhline(0, color='black', linestyle='--')
plt.axvline(0, color='black', linestyle='--')
plt.plot(orbit_straight_line[0], orbit_straight_line[1])
plt.scatter(orbit_straight_line[0][::100], orbit_straight_line[1][::100], color='red')  # Points rouges aux sauts de 0.1 an
plt.title('Ligne droite (e = 0, i = π/2)')
plt.axis('equal')

plt.subplot(3, 2, 3)
plt.axhline(0, color='black', linestyle='--')
plt.axvline(0, color='black', linestyle='--')
plt.plot(orbit_inclination[0], orbit_inclination[1])
plt.scatter(orbit_inclination[0][::100], orbit_inclination[1][::100], color='red')  # Points rouges aux sauts de 0.1 an
plt.title('Effet de l\'inclinaison')
plt.axis('equal')

plt.subplot(3, 2, 4)
plt.axhline(0, color='black', linestyle='--')
plt.axvline(0, color='black', linestyle='--')
plt.plot(orbit_excentricity[0], orbit_excentricity[1])
plt.scatter(orbit_excentricity[0][::100], orbit_excentricity[1][::100], color='red')  # Points rouges aux sauts de 0.1 an
plt.title('Effet de l\'excentricité')
plt.axis('equal')

plt.subplot(3, 2, 5)
plt.axhline(0, color='black', linestyle='--')
plt.axvline(0, color='black', linestyle='--')
plt.plot(orbit_rotation[0], orbit_rotation[1])
plt.scatter(orbit_rotation[0][::100], orbit_rotation[1][::100], color='red')  # Points rouges aux sauts de 0.1 an
plt.title('Effet des angles Ω, i, et ω')
plt.axis('equal')

plt.tight_layout()
plt.savefig('effetdediffparams.png')
plt.show()



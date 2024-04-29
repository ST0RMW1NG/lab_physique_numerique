# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 17:09:25 2023

@author: teemo
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Constante gravitationnelle
G = 4 * np.pi**2  # en AU**3 Msol**-1 annee**-2

# Masse de l'etoile
M = 1  # en masse solaire

# Termes de droite des EDO
def g(t, f):
    x, y, u, v = f
    r = np.sqrt(x**2 + y**2)
    dxdt = u
    dydt = v
    dudt = -G * M * x / (r**3)
    dvdt = -G * M * y / (r**3)
    return [dxdt, dydt, dudt, dvdt]

# Parametres de l'integration
h = 0.01  # annees
tmax = 20  # annees

# Initialisation du tableau de temps
t = np.arange(0, tmax + h/2, h)

# Condition initiale
R = 1.0  # rayon circulaire en AU
f0 = [0, -R, np.sqrt(G * M / R), 0]

# Resolution des ODEs
sol = solve_ivp(g, (t[0], t[-1]), f0, t_eval=t, first_step=h, max_step=h)
x = sol.y[0]  # position en x (AU)
y = sol.y[1]  # position en y (AU)
u = sol.y[2]  # vitesse en x
v = sol.y[3]  # vitesse en y

# Graphique
plt.plot(x, y)
plt.scatter(0, 0, color='red', marker='*', s=500)
plt.xlabel('x (AU)')
plt.ylabel('y (AU)')
plt.axhline(0, color='k', linestyle='--')
plt.axvline(0, color='k', linestyle='--')
plt.axis('equal')
plt.title('Orbite circulaire')
plt.savefig('20279063lab8.1.png')
plt.show()
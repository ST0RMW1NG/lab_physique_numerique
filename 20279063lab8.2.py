# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 17:09:25 2023

@author: teemo
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp



#cste gravitationnelle
G=4*np.pi**2 #en AU**3 Msol**-1 annee**-2

#mass de l'etoile 
M=1 #en masse solaire

#les termes de droites des EDO

def g(t,f):
    x, y, u, v = f
    r = np.sqrt(x**2 + y**2)
    dxdt = u
    dydt = v
    dudt = -G * M * x / (r**3)
    dvdt = -G * M * y / (r**3)
    return [dxdt, dydt, dudt, dvdt]


#param de l'inte
h=0.001 #annees
tmax=100 #annees

#initi du tbleau de temps
t=np.arange(0,tmax+h/2, h)

#condition initiale
R = 1.0 #rayon circulaire en AU
f0 = [0, -R, 0.9*np.sqrt(G * M / R), 0]


#resolution des ODEs
sol=solve_ivp(g,(t[0], t[-1]), f0, t_eval=t, first_step=h, max_step=h)
x = sol.y[0]  # position en x (AU)
y = sol.y[1]  # position en y (AU)
u = sol.y[2]  # vitesse en x
v = sol.y[3]  # vitesse en y

#graph de l'orbite
plt.plot(x,y)
plt.xlabel('x (AU)')
plt.ylabel('y (AU)')
plt.scatter(0, 0, color='red', marker='*', s=500)
plt.axhline(0, color='black', linestyle='--')
plt.axvline(0, color='black', linestyle='--')
plt.axis('equal')
plt.title('orbite elipse')
plt.savefig('lab8orbiteelipse.png')
plt.show()

#graph du rayon
r=  np.sqrt(x**2 + y**2)
plt.plot(t, r)
plt.xlabel('t (annees)')
plt.ylabel('r (AU)')
plt.legend()
plt.savefig('lab8rayonft.png')
plt.show()
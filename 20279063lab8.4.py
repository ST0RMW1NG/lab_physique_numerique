# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 17:09:49 2023

@author: teemo
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Cste
G = 4 * np.pi**2  #cste gravitationnel
M0 = 1.  #masse de l'étoile centrale en masse solaire
R1 = 1.  #rayon initial de super jupiter en AU
R2 = 1.22  #rayon initial de secundus en AU
M1= 0.01 #masse super-jupiter
M2= 0.001 #masse secundus (2ieme planete)
tmax = 100 #temps max de la simulation
h = 0.001  #pas de temps 


#les termes de droites des EDO

def g(t, f):
    x1, y1, u1, v1, x2, y2, u2, v2 = f

    r1 = np.sqrt(x1**2 + y1**2) #distance radial de super jupiter
    r2 = np.sqrt(x2**2 + y2**2) #distance radial de secundus

    # Equation  super-Jupiter
    dx1_dt = u1
    dy1_dt = v1
    du1_dt = -((G * M0 * x1) / (r1**3)) - ((G * M2) * (x1 - x2) / ((x2 - x1)**2 + (y2 - y1)**2)**(3 / 2))
    dv1_dt = -G * M0 * y1 / (r1**3) - (G * M2) * (y1 - y2) / ((x2 - x1)**2 + (y2 - y1)**2)**(3 / 2)

    # Equation secundus
    dx2_dt = u2
    dy2_dt = v2
    du2_dt = -G * M0 * x2 / (r2**3) - (G * M1 * (x2 - x1) / ((x2 - x1)**2 + (y2 - y1)**2)**(3 / 2))
    dv2_dt = -G * M0 * y2 / (r2**3) - (G * M1 * (y2 - y1) / ((x2 - x1)**2 + (y2 - y1)**2)**(3 / 2))

    return [dx1_dt, dy1_dt, du1_dt, dv1_dt, dx2_dt, dy2_dt, du2_dt, dv2_dt]

#condition initiale
f0 = [0., -R1, 0.9 * np.sqrt(G * M0 / R1), 0., 0., -R2, 2 * np.pi * np.sqrt(M0/R2), 0.]

#initi du tbleau de temps
t = np.arange(0, tmax + h / 2, h)

# Resolution des ODEs
sol = solve_ivp(g, (t[0], t[-1]), f0, t_eval=t, first_step=h, max_step=h)


#param 
x1= sol.y[0]
y1= sol.y[1]
u1= sol.y[2]
v1= sol.y[3]
x2= sol.y[4]
y2= sol.y[5]
u2=sol.y[6]
v2= sol.y[7]

#graph
plt.figure(figsize=(8, 8))
plt.plot(x1, y1, label='super-jupiter')
plt.scatter(0, 0, color='red', marker='*', s=500)
plt.plot(x2, y2, label='secundus')
plt.xlabel('x(AU)')
plt.ylabel('y(AU)')
plt.axis('equal')
plt.axhline(0, color='black', linestyle='--')
plt.axvline(0, color='black', linestyle='--')
plt.title('Orbite des planetes')
plt.legend()
plt.savefig('orbite secundus2.png')
plt.show() 

#graph de la distamce radial de super jupiter
r1=  np.sqrt(x1**2 + y1**2)
plt.plot(t, r1, label='super-jupiter')
plt.xlabel('t (annees)')
plt.ylabel('r (AU)')
plt.legend()
plt.show()

#graph de la distance radial de secundus
r2 = np.sqrt(x2**2 + y2**2)
plt.plot(t, r2, label='secundus')
plt.xlabel('t (annees)')
plt.ylabel('r (AU)')
plt.legend()
plt.savefig('rayon secundus2.png')
plt.show()
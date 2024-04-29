# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 19:54:32 2023

@author: teemo
"""

import numpy as np

#1000 valeurs aléatoires
random_M = np.random.uniform(0, 4 * np.pi, 1000)
random_e = np.random.rand(1000)
epsilon = 1.e-10


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

# Vérification pour les valeurs aléatoires
for M_value, e_value in zip(random_M, random_e):
    E_result = calc_anom_exc(M_value, e_value)
    equation_result = E_result - e_value * np.sin(E_result) - M_value

    # Vérifier que le résultat est proche de zéro
    assert np.allclose(equation_result, 0, atol=epsilon), f"Validation échouée pour M={M_value}, e={e_value}"

# Vérification pour M = e = 0
E_result_1 = calc_anom_exc(0, 0)
equation_result_1 = E_result_1 - 0 * np.sin(E_result_1) - 0
assert np.allclose(equation_result_1, 0, atol=epsilon), "Validation échouée pour M=0, e=0"

# Vérification pour M = 0. et e = 0.5
E_result_2 = calc_anom_exc(0.0, 0.5)
equation_result_2 = E_result_2 - 0.5 * np.sin(E_result_2) - 0.0
assert np.allclose(equation_result_2, 0, atol=epsilon), "Validation échouée pour M=0.0, e=0.5"


print("Validation success!")
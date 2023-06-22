# Author: Miko Mikarro
# -*- coding: utf-8 -*-

import numpy as np

import matplotlib.cm as cm
import matplotlib.pyplot as plt

def getRadius(index, n_1, n_2, r1, r2, r3):
    if index <= 0:
        return r1
    elif index >= n_1 + n_2 + 1:
        return r3
    else:
        width = getWidth(index, n_1, n_2, r1, r2, r3)
        if index <= n_1:
            return r1 + (r2 - r1) / n_1 * index - width/2
        else:
            return r2 + (r3 - r2) / n_2 * (index - n_1)  - width/2

def getWidth(index, n_1, n_2, r1, r2, r3):
    if index <= 0:
        return 0
    elif index >= n_1 + n_2 + 2:
        return 0
    else:
        if index <= n_1:
            return (r2 - r1) / n_1
        else:
            return (r3 - r2) / n_2

def getDistance(index, n_1, n_2, r1, r2, r3, direction):
    other_inc = 1 if direction == 'east' else -1
    current_r = getRadius(index, n_1, n_2, r1, r2, r3)
    other_r = getRadius(index + other_inc, n_1, n_2, r1, r2, r3)
    return abs(other_r - current_r)

def getSurface(index, n_1, n_2, r1, r2, r3, direction):
    if index == 0:
        return 4 * np.pi * r1**2
    elif index == n_1 + n_2 + 2:
        return 4 * np.pi * r3**2
    else:
        current_r = getRadius(index, n_1, n_2, r1, r2, r3)
        width_r = getWidth(index, n_1, n_2, r1, r2, r3)
        if direction == 'east':
            return 4 * np.pi * (current_r + width_r/2)**2
        elif direction == 'west':
            return 4 * np.pi * (current_r - width_r/2)**2

        elif direction == 'point':
            return 4 * np.pi * current_r**2

def getVolume(index, n_1, n_2, r1, r2, r3):
    if index == 0:
        return 0
    if index == n_1 + n_2 + 2:
        return 0
    current_r = getRadius(index, n_1, n_2, r1, r2, r3)
    width = getWidth(index, n_1, n_2, r1, r2, r3)

    return 4/3 * np.pi * ((current_r + width/2)**3 - (current_r - width/2)**3)

def getQ(index, n_1, n_2, q_1, q_2):
    if index == 0:
        return 0
    if index == n_1 + n_2 + 2:
        return 0
    if index <= n_1:
            return q_1
    return q_2
        
def getLambda(index, n_1, n_2, lambda_1, lambda_2, direction):
    if index == 0:
        return lambda_1
    if index == n_1 + n_2 + 2:
        return lambda_2
    
    other_index = (index + 1) if direction == 'east' else (index - 1)

    current_lambda = lambda_1 if index <= n_1 else lambda_2
    other_lambda = lambda_1 if other_index <= n_1 else lambda_2

    dist_total = getDistance(index, n_1, n_2, r1, r2, r3, direction)

    current_width = getWidth(index, n_1, n_2, r1, r2, r3)
    other_width = getWidth(other_index, n_1, n_2, r1, r2, r3)

    new_lambda = dist_total / ((current_width/2) / current_lambda + (other_width/2) / other_lambda)

    return new_lambda
# Define the 3 radius of the sphere
r1 = 1 # [m]
r2 = 2 # [m]
r3 = 3 # [m]

#Define interior and exterior temperature
T_int = 0 # [°C]
T_ext = 100 # [°C]

#Define calor generado por fuente interna de cada esfera
q_1 = 0 # [W/m^3]
q_2 = -1e10 # [W/m^3]

# Define interior and exterior convection coefficient
alpha_int = 5e10 # [W/m^2K
alpha_ext = 1e10 # [W/m^2K]

# Define interior and exterior conduction coefficient
lambda_1 = 5e1    # [W/mK]
lambda_2 = 1e1    # [W/mK]

# Define interior and exterior number of nodes
n_1 = 50
n_2 = 50

# Define convergence criteria
epsilon = 1e-100

# Define intial temperature

T_init  = [T_int + (T_ext-T_int)*i/(n_1+n_2+2) for i in range (n_1 + n_2 + 2)]
T_init [0] = T_int
T_init [n_1 + n_2 + 1] = T_ext
T_next  = [0 for i in range (n_1 + n_2 + 2)]
a_e     = [0 for i in range (n_1 + n_2 + 2)]
a_w     = [0 for i in range (n_1 + n_2 + 2)]
b_p     = [0 for i in range (n_1 + n_2 + 2)]
a_p     = [0 for i in range (n_1 + n_2 + 2)]

# plot the radius of the sphere


error = []
iterations = 0
for i in range(n_1 + n_2 + 2):
    lambda_e = getLambda(i, n_1, n_2, lambda_1, lambda_2, 'east')
    lambda_w = getLambda(i, n_1, n_2, lambda_1, lambda_2, 'west')
    
    S_e = getSurface(i, n_1, n_2, r1, r2, r3, 'east')
    S_w = getSurface(i, n_1, n_2, r1, r2, r3, 'west')
    S_p = getSurface(i, n_1, n_2, r1, r2, r3, 'point')

    q_i = getQ(i, n_1, n_2, q_1, q_2)

    dPE = getDistance(i, n_1, n_2, r1, r2, r3, 'east')
    dPW = getDistance(i, n_1, n_2, r1, r2, r3, 'west')
    
    Vi = getVolume(i, n_1, n_2, r1, r2, r3)

    if i == 0:
        a_w_i = 0
        a_e_i = lambda_e * S_e / dPE
        a_p_i = a_w_i + a_e_i + alpha_int*S_p
        b_p_i = alpha_int*S_p*T_int
        
    elif i == n_1 + n_2 + 1:
        a_w_i = lambda_w * S_w / dPW
        a_e_i = 0
        a_p_i = a_w_i + a_e_i + alpha_ext*S_p
        b_p_i = alpha_ext*S_p*T_ext
    else:
        a_w_i = lambda_w * S_w / dPW
        a_e_i = lambda_e * S_e / dPE
        a_p_i = a_w_i + a_e_i
        b_p_i = q_i * Vi
    
    a_w[i] = a_w_i
    a_e[i] = a_e_i
    a_p[i] = a_p_i
    b_p[i] = b_p_i

while True:
    for i in range(n_1 + n_2 + 2):
        if i == 0:
            T_next[i] = (b_p[i] + a_e[i]*T_init[i+1]) / a_p[i]
        elif i == n_1 + n_2 + 1:
            T_next[i] = (b_p[i] + a_w[i]*T_next[i-1]) / a_p[i]
        else:
            T_next[i] = (b_p[i] + a_w[i]*T_init[i-1] + a_e[i]*T_next[i+1]) / a_p[i]

    iterations += 1
    error.append(sum(abs(np.array(T_next) - np.array(T_init))))
    if (error[-1] < epsilon) and iterations > 1000:
        break

    T_init = T_next[:]
print("Acabé de calcular la temperatura en la esfera")
# Plot the temperature distribution in the sphere by 2d circles
x = [0 for i in range(n_1 + n_2 + 2)]
y = [0 for i in range(n_1 + n_2 + 2)]
r = [0 for i in range(n_1 + n_2 + 2)]
for i in range(n_1 + n_2 + 2):
    if i == 0:
        x[i] = 0
        y[i] = 0
        r[i] = r1
    elif i == n_1 + n_2 + 1:
        x[i] = 0
        y[i] = 0
        r[i] = r3
    else:
        if i <= n_1:
            x[i] = 0
            y[i] = 0
            r[i] = r1 - (r1 - r2) / n_1 * (i - 1)
        else:
            x[i] = 0
            y[i] = 0
            r[i] = r2 - (r2 - r3) / n_2 * (i - n_1 - 1)
        
fig, ax = plt.subplots()
for i in list(range(n_1 + n_2 + 2))[::-1]:
    color = cm.jet((T_next[i] - min(T_next)) / (max(T_next) - min(T_next)))
    circle = plt.Circle((x[i], y[i]), r[i], color=color )
    ax.add_artist(circle)
    
ax.set_xlim([-3, 3])
ax.set_ylim([-3, 3])

plt.show()

# Plot the temperature distribution in the sphere
plt.plot([getRadius(i, n_1, n_2, r1, r2, r3) for i in range(len(T_next))],T_next)
plt.show()

# Plot the error
plt.plot(np.log10(range(len(error))),np.log10(error))
print("El error es: ", error[-1])
plt.show()

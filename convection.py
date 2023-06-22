import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt

def get_cross_section(r):
    return np.pi * r**2

def get_lateral_area(r1, r2, dx):
    return np.pi * (r1 + r2) * np.sqrt((r2 - r1)**2 + dx**2)

def get_angle(r1, r2, dx):
    return np.arctan2(r2 - r1, dx)

def get_sgen(T1, T2, P1, P2, Cp, Rg):
    return Cp * np.log(T2 / T1) - Rg * (P2 / P1)
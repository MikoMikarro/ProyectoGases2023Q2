import numpy as np
from scipy.interpolate import interp1d
T_copper = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 30, 40, 50, 60, 70, 80, 90, 100, 150, 200, 250, 300, 350, 400, 500, 600, 800, 1000, 1200,  10000])
lambda_copper_vals = np.array([4220, 8400, 12500, 16200, 19500, 22200, 23900, 24800, 24900, 24300, 17100, 10800, 4450, 2170, 1250, 829, 647, 557, 508, 482, 429, 413, 406, 401, 396, 393, 386, 379, 366, 352, 339, 339])
lambda_copper_curve = interp1d(T_copper, lambda_copper_vals)


def cp_h2o(T):
    var_cp = 0.4198640560e+01 + -0.2036434100e-02 * T + 0.6520402110e-05 * T**2 + -0.5487970620e-08 * T**3 + 0.1771978170e-11 * T**4
    return 3.814 * var_cp

def lambda_h2o(T):
    var_lam = 0.1185254026e+02 + -0.8965822807e+01 * np.log(T) + 0.1528828068e+01 * np.log(T)**2 + -0.7590175979e-01 * np.log(T)**3
    return np.exp(var_lam)

def mu_h2o(T):
    var_mu = -0.1286013492e+02 + -0.1377850379e+01 * np.log(T) + 0.4213981638e+00 * np.log(T)**2 + -0.2414423056e-01 * np.log(T)**3
    return np.exp(var_mu)

def cp_avg_h2o(T1, T2):
    int_t1 = 0.4198640560e+01 * T1 + 2 * -0.2036434100e-02 * T1**2 + 3 * 0.6520402110e-05 * T1**3 + 4 * -0.5487970620e-08 * T1**4 + 5 * 0.1771978170e-11 * T1**5
    int_t2 = 0.4198640560e+01 * T2 + 2 * -0.2036434100e-02 * T2**2 + 3 * 0.6520402110e-05 * T2**3 + 4 * -0.5487970620e-08 * T2**4 + 5 * 0.1771978170e-11 * T2**5
    return 8.314 * (int_t2 - int_t1) / (T2 - T1)

def lambda_copper(T):
        t = [T]
        lambda_val = lambda_copper_curve(t)
        return lambda_val[0]
import numpy as np

from main import p_in_interior, T_in_interior, v_in_interior
from gas_properties import cp_h2o, lambda_h2o, mu_h2o
from CONSTANTS import length, epsilon_r


def converge_interior_fluid(slices):

    Rg = 8.314 / 0.018015 # J/kgK (R g of water vapor)
    Trstart = 3700

    iteration_slices = deepcopy(slices)

    # Inlet conditions
    iteration_slices[0].p_interior_fluid = p_in_interior
    iteration_slices[0].T_interior_fluid = T_in_interior
    iteration_slices[0].v_interior_fluid = v_in_interior
    iteration_slices[0].rho_interior_fluid = p_in_interior / (T_in_interior * Rg)
    m_dot = iteration_slices[0].cross_section * iteration_slices[0].rho_interior_fluid * v_in_interior

    # Iterate through nodes
    for slice, i in enumerate(iteration_slices):
        #Starting conditions
        iteration_slices[i].Tr_interior_fluid    = Tr_start
        iteration_slices[i+1].p_interior_fluid   = iteration_slices[i].p_interior_fluid
        iteration_slices[i+1].T_interior_fluid   = iteration_slices[i].T_interior_fluid
        iteration_slices[i+1].v_interior_fluid   = iteration_slices[i].v_interior_fluid
        iteration_slices[i+1].rho_interior_fluid = iteration_slices[i].rho_interior_fluid

        #Iterate until convergence
        while True:
            # Estimated reference values
            Ti   = (iteration_slices[i+1].p_interior_fluid + iteration_slices[i].p_interior_fluid)/2
            vi   = (iteration_slices[i+1].v_interior_fluid + iteration_slices[i].v_interior_fluid)/2
            Pi   = (iteration_slices[i+1].p_interior_fluid + iteration_slices[i].p_interior_fluid)/2
            Tref = (Ti + slice.T_interior_wall)/2 + 0.22 * (iteration_slices[i].Tr - Ti)

            # Thermpphysical properties
            rhoi    = Pi / (Tref * Rg)
            cpi     = cp_h2o(Tref)
            lambdai = lambda_h2o(Tref)
            mui     = mu_h2o(Tref)

            # Other properties
            Di = 2 * (iteration_slices[i+1].radius + iteration_slices[i].radius)/2

            #   Empyrical coefficients
            Re = rhoi * vi *  Di / mui
            Pr = mui * cpi / lambdai
            Gz = Re * Pr * Di / length

            # Nusselt
            if  Re < 2000 and Gz > 10:
                nu_c = [1.86, 1/3, 1/3, (Di/length)**(1/3) * (mui / mu_h20(slice.T_interior_wall))**0.14]
            elif  Re < 2000 and Gz < 10:
                nu_c = [3.66, 0, 0, 1]
            else:
                nu_c = [3.66, 0, 0, 1]
            Nu = nu_c[0] * Re**nu_c[1] * Pr**nu_c[2] * nu_c[3]

            # Convective heat transfer coefficient
            alpha = Nu * lambdai / Di

            # Friction factor (Churchill expression)
            fA = (2.475 * np.log(1 / ((7 / Re)**0.9 + 0.27*epsilon_r)))**16
            fB = (37530 / Re)**16
            f = 2 * ((8 / Re)**12 + 1 / (fA + fB)**(3 / 2))**(1/12)

    
    return iteration_slices
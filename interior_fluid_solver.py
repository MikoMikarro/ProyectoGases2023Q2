from main import p_in_interior, T_in_interior, v_in_interior
from copy import deepcopy
from gas_properties import cp_h2o, lambda_h2o, mu_h2o


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
            Rei = rhoi * vi *  Di / mui
            Pri = mui * cpi / lambdai

            


    
    return iteration_slices
import numpy as np

from gas_properties import cp_h2o, lambda_h2o, mu_h2o, cp_avg_h2o
from copy import deepcopy
from CONSTANTS import length, epsilon_r,convergence_T


def converge_interior_fluid(slices, p_in_interior, T_in_interior, v_in_interior, p_in_exterior):
    # Calculates the interior fluid properties throughout the nozzle

    Rg = 8.314 / 0.018015 # J/kgK (R g of water vapor)
    Tr_start = 3700

    iteration_slices = deepcopy(slices)

    # Inlet conditions
    iteration_slices[0].p_interior_fluid = p_in_interior
    iteration_slices[0].T_interior_fluid = T_in_interior
    iteration_slices[0].v_interior_fluid = v_in_interior
    iteration_slices[0].rho_interior_fluid = p_in_interior / (T_in_interior * Rg)
    m_dot = iteration_slices[0].cross_section_interior_fluid * iteration_slices[0].rho_interior_fluid * v_in_interior

    # Iterate through nodes
    for i, slice in enumerate(iteration_slices[:-1]):
        #Starting conditions
        iteration_slices[i].Tr_interior_fluid    = Tr_start
        iteration_slices[i+1].p_interior_fluid   = iteration_slices[i].p_interior_fluid
        iteration_slices[i+1].T_interior_fluid   = iteration_slices[i].T_interior_fluid + 100 # To avoid div by 0 on first iteration
        iteration_slices[i+1].v_interior_fluid   = iteration_slices[i].v_interior_fluid
        iteration_slices[i+1].rho_interior_fluid = iteration_slices[i].rho_interior_fluid

        #Iterate until convergence
        while True:
            # Estimated reference values
            Ti   = (iteration_slices[i+1].T_interior_fluid + iteration_slices[i].T_interior_fluid)/2
            vi   = (iteration_slices[i+1].v_interior_fluid + iteration_slices[i].v_interior_fluid)/2
            Pi   = (iteration_slices[i+1].p_interior_fluid + iteration_slices[i].p_interior_fluid)/2
            Tref = (Ti + slice.T_interior_wall)/2 + 0.22 * (iteration_slices[i].Tr_interior_fluid - Ti)

            # Thermpphysical properties
            rhoi    = Pi / (Tref * Rg)
            cpi     = cp_h2o(Tref)
            lambdai = lambda_h2o(Tref)
            mui     = mu_h2o(Tref)

            # Other properties
            Di = iteration_slices[i+1].radius_interior_fluid + iteration_slices[i].radius_interior_fluid

            #   Empyrical coefficients
            Re = rhoi * vi *  Di / mui
            Pr = mui * cpi / lambdai
            Gz = Re * Pr * Di / length

            # Recuperation factor
            if Re < 2000:        # Laminar
                r = Pr**(1/2)
            elif Re >= 2000:     # Turbulent
                r = Pr**(1/3) 

            # Nusselt
            if  Re < 2000 and Gz > 10:
                nu_c = [1.86, 1/3, 1/3, (Di/length)**(1/3) * (mui / mu_h2o(slice.T_interior_wall))**0.14]
            
            elif  Re < 2000 and Gz < 10:
                nu_c = [3.66, 0, 0, 1]
            else:
                nu_c = [3.66, 0, 0, 1]
            Nu = nu_c[0] * Re**nu_c[1] * Pr**nu_c[2] * nu_c[3]
            print(iteration_slices[i].radius_interior_fluid)

            # Convective heat transfer coefficient
            alpha = Nu * lambdai / Di

            # Friction factor (Churchill expression)
            fA = (2.475 * np.log(1 / ((7 / Re)**0.9 + 0.27*epsilon_r)))**16
            fB = (37530 / Re)**16
            f = 2 * ((8 / Re)**12 + 1 / (fA + fB)**(3 / 2))**(1/12)

            # Average Cp heat coefficients
            cpr_avg = cp_avg_h2o(iteration_slices[i].Tr_interior_fluid, slice.T_interior_wall)
            cpi_avg = cp_avg_h2o(iteration_slices[i].T_interior_fluid, iteration_slices[i+1].T_interior_fluid)

            # Linealized moment equation coefficients for solving the outlet velocity
            Am = m_dot + f * rhoi * vi / 4 * slice.lateral_area_interior_fluid * np.cos(slice.angle)
            Bm = (iteration_slices[i+1].cross_section_interior_fluid + iteration_slices[i].cross_section_interior_fluid)/2
            Cm = m_dot * slice.v_interior_fluid + slice.p_interior_fluid * (iteration_slices[i+1].cross_section_interior_fluid - iteration_slices[i].cross_section_interior_fluid)/2 + slice.p_interior_fluid * iteration_slices[i].cross_section_interior_fluid - f * rhoi * vi / 4 * slice.lateral_area_interior_fluid * np.cos(slice.angle) * iteration_slices[i].v_interior_fluid

            # Linealized energy equation coefficients for solving the outlet velocity
            Ae = m_dot * cpi_avg + alpha / 2 * slice.lateral_area_interior_fluid
            Be = m_dot/2 + alpha * r / (4 * cpr_avg) * slice.lateral_area_interior_fluid
            Ce = slice.T_interior_fluid * (m_dot * cpi_avg - alpha/2 * slice.lateral_area_interior_fluid) + slice.v_interior_fluid**2 * (m_dot - alpha * r / (4 * cpr_avg) * slice.lateral_area_interior_fluid) + slice.T_interior_wall * alpha * slice.lateral_area_interior_fluid
            
            # Linealized overall coefficients for solving the outlet velocity
            A = Am * Ae * iteration_slices[i+1].cross_section_interior_fluid - Rg * m_dot * Bm * Be
            B = - Cm * Ae * iteration_slices[i+1].cross_section_interior_fluid
            C = Bm * Ce * Rg * m_dot

            # If negative discriminant return nonsense value
            if B**2 - 4 * A * C:
                iteration_slices[i].Tr_interior_fluid  = -1
                iteration_slices[i].p_interior_fluid   = -1
                iteration_slices[i].T_interior_fluid   = -1
                iteration_slices[i].v_interior_fluid   = -1
                iteration_slices[i].rho_interior_fluid = -1
                return iteration_slices
            
            else:
                # Calculation of possible velocity values
                vout_p = (B + (B**2 - 4 * A * C)) / (2 * A) # Valor sqrt de discriminante positivo
                vout_n = (B - (B**2 - 4 * A * C)) / (2 * A) # Valor sqrt de discriminante negativo

                # Calculation of possible pressure values
                pout_p = (Cm - vout_p * Am) / Bm
                pout_n = (Cm - vout_n * Am) / Bm

                # Calculation of possible temperature values
                Tout_p = (Ce - vout_p**2 * Be) / Ae
                Tout_n = (Ce - vout_n**2 * Be) / Ae

                # Generated entropy for each case
                Sgen_p = cpi_avg * np.log(Tout_p / iteration_slices[i].T_interior_fluid) - Rg * (pout_p / iteration_slices[i].p_interior_fluid)
                Sgen_n = cpi_avg * np.log(Tout_n / iteration_slices[i].T_interior_fluid) - Rg * (pout_n / iteration_slices[i].p_interior_fluid)

                # Supersonic case (Summerfield criterion is applied to determine if and where the shockwave occurs)
                if Sgen_p >= 0 and Sgen_n >= 0:
                    
                    # Determine which pressure corresponds to the shock
                    if abs(iteration_slices[i].p_interior_fluid - pout_p) > abs(iteration_slices[i].p_interior_fluid - pout_n):
                        p_shock = pout_p
                        v_shock = vout_p
                        T_shock = Tout_p
                        p_cont = pout_n
                        v_cont = vout_n
                        T_cont = Tout_n
                    else:
                        p_shock = pout_n
                        v_shock = vout_n
                        T_shock = Tout_n
                        p_cont = pout_p
                        v_cont = vout_p
                        T_cont = Tout_p
                    
                    # Case where shockwave occurs inside nozzle
                    if p_cont < 0.4 * p_in_exterior and i < len(iteration_slices) - 1:
                        pout = p_shock
                        vout = v_shock
                        Tout = T_shock

                    # Case where shockwave occurs outside the nozzle                    
                    elif p_cont < p_in_exterior and i == len(iteration_slices) - 1:
                        pout = p_shock
                        vout = v_shock
                        Tout = T_shock

                    # Case where no shockwave occurs
                    else:
                        pout = p_cont
                        vout = v_cont
                        Tout = T_cont

                # Subsonic case p (only a generated entropy is positive, there cannot be a shock wave)
                elif Sgen_p >= 0:
                    vout = vout_p
                    pout = pout_p
                    Tout = Tout_p

                # Subsonic case n (only a generated entropy is positive, there cannot be a shock wave)
                elif Sgen_n >= 0:
                    vout = vout_n
                    pout = pout_n
                    Tout = Tout_n
                
                # Calculate recovery temperature and assign properties to the exit node
                Ti = (iteration_slices[i].T_interior_fluid + Tout)/2
                vi = (iteration_slices[i].v_interior_fluid + vout)/2
                iteration_slices[i+1].Tr_interior_fluid  = Ti + vi**2 / (2 * cpr_avg)
                iteration_slices[i+1].p_interior_fluid   = pout
                iteration_slices[i+1].T_interior_fluid   = Tout
                iteration_slices[i+1].v_interior_fluid   = vout
                iteration_slices[i+1].rho_interior_fluid = m_dot / (vout * iteration_slices[i+1].cross_section_interior_fluid)

                # Check convergence
                if abs(iteration_slices[i+1].Tr_interior_fluid - iteration_slices[i].Tr_interior_fluid) < convergence_T:
                    print(vout)
                    break
    
    return iteration_slices
from utils import geometric_avg
from copy import deepcopy

def converge_exterior_wall(slices, alpha_env, T_env):

    iteration_slices = deepcopy(slices)
    start_slices = deepcopy(iteration_slices)
    while True:
        for i in range(len(start_slices)):
            old_temp = start_slices[i].T_exterior_wall
            new_temp = iteration_slices[i].T_exterior_wall
            delta_T = new_temp - old_temp
            start_slices[i].T_exterior_wall = 1.5*delta_T + old_temp

        iteration_slices = deepcopy(start_slices)
        
        for i, slice in enumerate(iteration_slices[:-1]):
            start_slice = deepcopy(slice)
            iteration_slice = deepcopy(start_slice)
                
            alpha_int = iteration_slice.alpha_exterior_fluid
            A_int = iteration_slice.lateral_area_interior_fluid
            T_int = iteration_slice.T_exterior_fluid

            ad = alpha_int * A_int

            alpha_ext = alpha_env
            A_ext = slice.lateral_area_exterior_wall
            T_ext = T_env

            au = alpha_ext * A_ext
            
            east_slice = iteration_slices[i+1]

            d_e = slice.dx
            d_w = slice.dx
            A_w = slice.cross_section_interior_wall
            T_e = east_slice.T_exterior_wall
            A_e = east_slice.cross_section_interior_wall

            while True:
                start_slice = deepcopy(iteration_slice)
                iteration_slice = deepcopy(start_slice)
                
                if i == 0:
                    T_w = 0
                    aw = 0
                    lambda_e = geometric_avg(east_slice.lambda_exterior_wall, iteration_slice.lambda_exterior_wall, east_slice.dx, iteration_slice.dx)
                    ae = lambda_e * A_e / d_e
                    
                else:
                    west_slice = iteration_slices[i-1]
                    lambda_w = geometric_avg(west_slice.lambda_exterior_wall, iteration_slice.lambda_exterior_wall, west_slice.dx, iteration_slice.dx)
                    T_w = west_slice.T_exterior_wall
                    aw = lambda_w * A_w / d_w

                    if i ==len(iteration_slices) - 1:
                        T_e = T_env
                        alpha_e = alpha_env
                        ae = alpha_e * T_e

                    else:
                        lambda_e = geometric_avg(east_slice.lambda_exterior_wall, iteration_slice.lambda_exterior_wall, east_slice.dx, iteration_slice.dx)
                        T_e = east_slice.T_exterior_wall
                        ae = lambda_e * A_e / d_e
                    

                iteration_slice.T_exterior_wall = (aw * T_w + ad * T_int + au * T_ext + ae * T_e) / (aw + ad + ae + au)

                if not iteration_slice.not_converges(start_slice):
                    break

            iteration_slices[i] = iteration_slice
        converged = True
        for i, new_slice in enumerate(iteration_slices):
            old_slice = start_slices[i]
            if old_slice.not_converges(new_slice):
                converged = False
                break
        
        if converged:
            break

    return iteration_slices
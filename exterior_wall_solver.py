from utils import geometric_avg
from copy import deepcopy

def converge_exterior_wall(slices, alpha_env, T_env):

    iteration_slices = deepcopy(slices)
    while True:
        
        start_slices = deepcopy(iteration_slices)
        iteration_slices = deepcopy(start_slices)
        
        for i, slice in enumerate(iteration_slices[:-1]):

            alpha_int = slice.alpha_exterior_fluid
            A_int = slice.lateral_area_exterior_fluid
            T_int = slice.T_exterior_fluid

            ad = alpha_int * A_int

            alpha_ext = alpha_env
            A_ext = slice.lateral_area_interior_wall
            T_ext = T_env

            au = alpha_ext * A_ext
            
            east_slice = iteration_slices[i+1]

            if i == 0:
                T_w = 0
                aw = 0
                
                lambda_e = geometric_avg(east_slice.lambda_exterior_wall, slice.lambda_exterior_wall, east_slice.dx, slice.dx)
                T_e = east_slice.T_exterior_wall
                A_e = east_slice.cross_section_exterior_wall
                d_e = slice.dx
                ae = lambda_e * A_e / d_e
                
            else:
                west_slice = iteration_slices[i-1]
                lambda_w = geometric_avg(west_slice.lambda_exterior_wall, slice.lambda_exterior_wall, west_slice.dx, slice.dx)
                T_w = west_slice.T_exterior_wall
                A_w = slice.cross_section_exterior_wall
                d_w = slice.dx

                aw = lambda_w * A_w / d_w

                if i ==len(iteration_slices) - 2:
                    T_e = T_env
                    alpha_e = alpha_env
                    A_e = east_slice.cross_section_exterior_wall
                    ae = alpha_e * T_e

                else:
                    lambda_e = geometric_avg(east_slice.lambda_exterior_wall, slice.lambda_exterior_wall, east_slice.dx, slice.dx)
                    T_e = east_slice.T_exterior_wall
                    A_e = east_slice.cross_section_exterior_wall
                    d_e = slice.dx
                    ae = lambda_e * A_e / d_e
            

            slice.T_interior_wall = (aw * T_w + ad * T_int + au * T_ext + ae * T_e) / (aw + ad+ ae + au)


        converged = True
        for i, new_slice in enumerate(iteration_slices):
            old_slice = start_slices[i]
            if old_slice.not_converges(new_slice):
                converged = False
                break
        
        if converged:
            break

    return iteration_slices
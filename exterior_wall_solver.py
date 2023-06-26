from utils import geometric_avg
from copy import deepcopy

def converge_exterior_wall(slices, T_in_exterior_wall, alpha_env, T_ext):

    iteration_slices = deepcopy(slices)
    while True:
        
        start_slices = deepcopy(iteration_slices)
        iteration_slices = deepcopy(start_slices)
        iteration_slices = iteration_slices[::-1]
        
        for i, slice in enumerate(iteration_slices[1:-1]):
            if i!= 0:
                lambda_w = geometric_avg(iteration_slices[i-1].lambda_exterior_wall, slice.lambda_exterior_wall, slice.dx/2, slice.dx/2)
                q_w = (slice.T_exterior_wall - iteration_slices[i-1].T_exterior_wall) * -lambda_w / slice.dx 

            else:
                lambda_w    = slice.lambda_exterior_wall
                q_w         = (slice.T_exterior_wall - T_in_exterior_wall) * -lambda_w / (slice.dx/2)

            A_w = slice.cross_section_exterior_wall
            lambda_e = geometric_avg(slice.lambda_exterior_wall, iteration_slices[i+1].lambda_exterior_wall, slice.dx/2, slice.dx/2)
            A_e = iteration_slices[i+1].cross_section_exterior_wall

            q_up = alpha_env*(slice.T_exterior_wall - T_ext)
            A_up = slice.lateral_area_interior_fluid

            q_down = slice.alpha_exterior_fluid*(slice.T_exterior_fluid - slice.T_exterior_wall)
            A_down = slice.lateral_area_exterior_wall

            iteration_slices[i+1].T_exterior_wall = (q_w*A_w - q_up*A_up + q_down*A_down) / (-lambda_e * A_e) + slice.T_exterior_wall

        iteration_slices = iteration_slices[::-1]

        converged = True
        
        for new_slice, i in enumerate(iteration_slices):
            old_slice = start_slices[i]
            if old_slice.not_converges(new_slice):
                converged = False
                break
        
        if converged:
            break
    
    return iteration_slices
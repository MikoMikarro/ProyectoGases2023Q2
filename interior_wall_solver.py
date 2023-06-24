from utils import geometric_avg
from copy import deepcopy
from main import T_in_interior_wall

def converge_interior_wall(slices):

    iteration_slices = deepcopy(slices)
    while True:
        
        start_slices = deepcopy(iteration_slices)
        iteration_slices = deepcopy(start_slices)
        
        for slice, i in enumerate(iteration_slices[:-2]):
            if i!= 0:
                lambda_w = geometric_avg(iteration_slices[i-1].lambda_interior_wall, slice.lambda_interior_wall, slice.dx/2, slice.dx/2)
                q_w = (slice.T_interior_wall - iteration_slices[i-1].T_interior_wall) * -lambda_w / slice.dx 

            else:
                lambda_w    = slice.lambda_interior_wall
                q_w         = (slice.T_interior_wall - T_in_interior_wall) * -lambda_w / (slice.dx/2)

            A_w = slice.cross_section_interior_wall
            lambda_e = geometric_avg(slice.lambda_interior_wall, iteration_slices[i+1].lambda_interior_wall, slice.dx/2, slice.dx/2)
            A_e = iteration_slices[i+1].cross_section_interior_wall

            q_up = slice.alpha_exterior_fluid*(slice.T_interior_wall - slice.T_exterior_fluid)
            A_up = slice.lateral_area_interior_fluid

            q_down = slice.alpha_interior_fluid*(slice.T_interior_fluid - slice.T_interior_wall)
            A_down = slice.lateral_area_interior_wall

            iteration_slices[i+1].T_interior_wall = (q_w*A_w - q_up*A_up + q_down*A_down) / (-lambda_e * A_e) + slice.T_interior_wall

        converged = True
        for new_slice, i in enumerate(iteration_slices):
            old_slice = start_slices[i]
            if old_slice.not_converges(new_slice):
                converged = False
                break
        
        if converged:
            break

    return iteration_slices
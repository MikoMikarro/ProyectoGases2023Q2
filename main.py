from CONSTANTS import num_elems
from geometric_functions import Slice
from copy import deepcopy
from interior_fluid_solver import converge_interior_fluid
from exterior_fluid_solver import converge_exterior_fluid
from interior_wall_solver  import converge_interior_wall
from exterior_wall_solver  import converge_exterior_wall
# Start conditions
p_in_interior = 30 # atm
T_in_interior = 3600 # K
v_in_interior = 120 # m/s

p_in_exterior = 1 # atm
T_in_exterior = 34 # K
v_in_exterior = 200 # m/s

T_in_interior_wall = 300 # K
T_in_exterior_wall = 200 # K

T_ext         = 312 # K
p_ext         = 1 # atm

alpha_env     = 32e-5 # 

def main():
    all_slices = [Slice(i) for i in range(num_elems + 1)]

    ## Start conditions
    for i in all_slices:
        i.p_interior_fluid = p_in_interior
        i.T_interior_fluid = T_in_interior
        i.v_interior_fluid = v_in_interior

        i.p_exterior_fluid = p_in_exterior
        i.T_exterior_fluid = T_in_exterior
        i.v_exterior_fluid = v_in_exterior

        i.T_interior_wall = T_in_interior
        i.T_exterior_wall = T_in_exterior
    iteration_slices = deepcopy(all_slices)
    while True:
        
        start_slices = deepcopy(iteration_slices)
        iteration_slices = deepcopy(start_slices)

        iteration_slices = converge_interior_fluid(iteration_slices)
        iteration_slices = converge_exterior_fluid(iteration_slices)
        iteration_slices = converge_interior_wall (iteration_slices, T_in_interior_wall)
        iteration_slices = converge_exterior_wall (iteration_slices, T_in_exterior_wall, alpha_env, T_ext)

        converged = True
        for new_slice, i in enumerate(iteration_slices):
            old_slice = start_slices[i]
            if old_slice.not_converges(new_slice):
                converged = False
                break
        
        if converged:
            break



    pass

if __name__ == '__main__':
    main()
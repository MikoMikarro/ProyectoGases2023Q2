from CONSTANTS import num_elems
from geometric_functions import Slice
from copy import deepcopy
from interior_fluid_solver import converge_interior_fluid
from exterior_fluid_solver import converge_exterior_fluid
from interior_wall_solver  import converge_interior_wall
from exterior_wall_solver  import converge_exterior_wall
from utils import do_all_plots
import yaml
# Start conditions
p_in_interior = 200 * 101325 # Pa
T_in_interior = 1600 # K
v_in_interior = 100 # m/s

p_in_exterior = 1 * 101325 # Pa
T_in_exterior = 250 # K
v_in_exterior = 20 # m/s

T_env         = 500 # K

alpha_env     = 1200 # 

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

        i.T_interior_wall = T_env
        i.T_exterior_wall = T_env

    iteration_slices = deepcopy(all_slices)
    iteration = 0
    while True:
        
        start_slices = deepcopy(iteration_slices)
        iteration_slices = deepcopy(start_slices)

        iteration_slices = converge_interior_fluid(iteration_slices, p_in_interior, T_in_interior, v_in_interior, p_in_exterior)   
        iteration_slices = converge_exterior_fluid(iteration_slices)
        iteration_slices = converge_interior_wall (iteration_slices, alpha_env, T_env)
        iteration_slices = converge_exterior_wall (iteration_slices, alpha_env, T_env)

        print(iteration)
        iteration += 1
        converged = True
        for i, new_slice in enumerate(iteration_slices):
            old_slice = start_slices[i]
            if old_slice.not_converges(new_slice):
                converged = False
                break
        
        if converged:
            break
    
    all_slices = deepcopy(iteration_slices[:-1])

    ## Export all data

    data = {"T_interior_fluid": [float(i.T_interior_fluid) for i in all_slices],
            "x_position"      : [float(i.x               ) for i in all_slices],
            "radius_interior_fluid": [i.radius_interior_fluid for i in all_slices]}

    with open('data.yml', 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)

    do_all_plots(all_slices)


if __name__ == '__main__':
    main()
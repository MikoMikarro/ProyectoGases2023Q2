from CONSTANTS import num_elems
from geometric_functions import Slice
from copy import deepcopy
from interior_fluid_solver import converge_interior_fluid
from exterior_fluid_solver import converge_exterior_fluid
from interior_wall_solver  import converge_interior_wall
from exterior_wall_solver  import converge_exterior_wall

import matplotlib.pyplot as plt

# Start conditions
p_in_interior = 300 * 101325 # Pa
T_in_interior = 3300 # K
v_in_interior = 60 # m/s

p_in_exterior = 1 * 101325 # Pa
T_in_exterior = 34 # K
v_in_exterior = 20 # m/s

T_env         = 1000 # K

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
    
    all_slices = deepcopy(iteration_slices)

    # plot all temperatures
    plt.figure()
    plt.title('Temperature')
    plt.xlabel('x [m]')
    plt.ylabel('T [K]')
    plt.grid()
    plt.plot([i.x for i in all_slices], [i.T_interior_fluid for i in all_slices], label='T interior fluid')
    #plt.plot([i.x for i in all_slices], [i.T_exterior_fluid for i in all_slices], label='T exterior fluid')
    plt.plot([i.x for i in all_slices], [i.T_interior_wall for i in all_slices], label='T interior wall')
    plt.plot([i.x for i in all_slices], [i.T_exterior_wall for i in all_slices], label='T exterior wall')
    plt.legend()

    # plot all pressures
    plt.figure()
    plt.title('Pressure')
    plt.xlabel('x [m]')
    plt.ylabel('p [Pa]')
    plt.grid()
    plt.plot([i.x for i in all_slices], [i.p_interior_fluid for i in all_slices], label='p interior fluid')
    #plt.plot([i.x for i in all_slices], [i.p_exterior_fluid for i in all_slices], label='p exterior fluid')
    plt.legend()

    # plot all velocities
    plt.figure()
    plt.title('Velocity')
    plt.xlabel('x [m]')
    plt.ylabel('v [m/s]')
    plt.grid()
    plt.plot([i.x for i in all_slices], [i.v_interior_fluid for i in all_slices], label='v interior fluid')
    #plt.plot([i.x for i in all_slices], [i.v_exterior_fluid for i in all_slices], label='v exterior fluid')
    plt.legend()

    plt.show()


if __name__ == '__main__':
    main()
from matplotlib import pyplot as plt

def geometric_avg(v1, v2 , d1, d2):
    return d1/(d1/(2*v1) + d2*(2*v2))

def do_all_plots(all_slices):
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

    # plot all velocities
    plt.figure()
    plt.title('Mach')
    plt.xlabel('x [m]')
    plt.ylabel('M')
    plt.grid()
    plt.plot([i.x for i in all_slices], [i.M_interior_fluid for i in all_slices], label='M interior fluid')
    #plt.plot([i.x for i in all_slices], [i.v_exterior_fluid for i in all_slices], label='v exterior fluid')
    plt.legend()

    # plot shape of the nozzle
    plt.figure()
    plt.title('Nozzle shape')
    plt.xlabel('x [m]')
    plt.ylabel('y [m]')
    plt.grid()
    plt.plot([i.x for i in all_slices], [i.radius_interior_fluid for i in all_slices])
    plt.plot([i.x for i in all_slices], [-i.radius_interior_fluid for i in all_slices])
    plt.legend()

    plt.show()



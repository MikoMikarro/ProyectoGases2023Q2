import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline
from CONSTANTS import inner_diameter, length, throat_diameter, outter_diameter, \
    grosor_pared_interior, grosor_fluido_exterior, grosor_pared_exterior, num_elems

from CONSTANTS import convergence_p, convergence_T, convergence_v

class Slice:
    def __init__(self, element_num) -> None:
        self.element_num = element_num
        self.num_elems = num_elems

        x1 = np.array([0, 10, 20 , 40, 50, length-20 , length])
        y1 = np.array([inner_diameter/2, inner_diameter/2, inner_diameter/2,  throat_diameter/2, \
                throat_diameter/2, outter_diameter/2,  outter_diameter/2])

        self.spline = CubicSpline(x1/100, y1/100)
        self.dx = length/num_elems

        self.p_interior_fluid       = 0
        self.T_interior_fluid       = 0
        self.rho_interior_fluid     = 0
        self.v_interior_fluid       = 0

        self.T_interior_wall        = 0

        self.p_exterior_fluid       = 0
        self.T_exterior_fluid       = 0
        self.rho_exterior_fluid     = 0
        self.v_exterior_fluid       = 0

        self.T_exterior_wall        = 0

    def lateral_area(self, extra_radius = 0):
        x_vals = [length/self.num_elems * self.element_num, length/self.num_elems * (self.element_num + 1)]
        r1, r2 = self.spline(x_vals)
        r1 += extra_radius
        r2 += extra_radius
        dx = length/self.num_elems
        return np.pi * (r1 + r2) * np.sqrt((r2 - r1)**2 + dx**2)

    @property
    def lateral_area_interior_fluid(self):
        self.lateral_area()

    @property
    def lateral_area_interior_wall(self):
        self.lateral_area(grosor_pared_interior / 100)
    
    @property
    def lateral_area_exterior_fluid(self):
        self.lateral_area((grosor_pared_interior + grosor_fluido_exterior)/100)

    @property
    def lateral_area_exterior_wall(self):
        self.lateral_area((grosor_pared_interior + grosor_fluido_exterior + grosor_pared_exterior \
                           )/100)
    
    @property
    def angle(self):
        x_vals = [length/self.num_elems * self.element_num, length/self.num_elems * (self.element_num + 1)]
        r1, r2 = self.spline(x_vals)
        dx = length/self.num_elems

        return np.arctan2(r2 - r1, dx)
    
    def cross_section(self, extra_radius = 0):
        x_vals = [length/self.num_elems * self.element_num]
        r = self.spline(x_vals) + extra_radius
        return np.pi * r**2
    
    @property
    def cross_section_interior_fluid(self):
        return self.cross_section()
    
    @property
    def cross_section_interior_wall(self):
        return self.cross_section(grosor_pared_interior / 100) - self.cross_section_interior_fluid
    
    @property
    def cross_section_exterior_fluid(self):
        return self.cross_section((grosor_pared_interior + grosor_fluido_exterior)/100) - self.cross_section_interior_wall - self.cross_section_interior_fluid
    @property
    def cross_section_exterior_wall(self):
        return self.cross_section((grosor_pared_interior + grosor_fluido_exterior + grosor_pared_exterior \
            )/100) - self.cross_section_exterior_fluid - self.cross_section_interior_wall - self.cross_section_interior_fluid

    @property
    def alpha_interior_fluid(self):
        return 0
    
    @property
    def alpha_exterior_fluid(self):
        return 0
    
    @property
    def lambda_interior_fluid(self):
        return 0
    
    @property
    def lambda_interior_wall(self):
        return 0
    
    @property
    def lambda_exterior_fluid(self):
        return 0
    
    @property
    def lambda_exterior_wall(self):
        return 0
    
    def not_converges(self, other_slice):
        return (abs(self.p_exterior_fluid - other_slice.p_exterior_fluid) > convergence_p) or \
               (abs(self.p_interior_fluid - other_slice.p_interior_fluid) > convergence_p) or \
               (abs(self.T_exterior_fluid - other_slice.T_exterior_fluid) > convergence_T) or \
               (abs(self.T_exterior_wall  - other_slice.T_exterior_wall)  > convergence_T) or \
               (abs(self.T_interior_fluid - other_slice.T_interior_fluid) > convergence_T) or \
               (abs(self.T_interior_wall  - other_slice.T_interior_wall)  > convergence_T) or \
               (abs(self.v_exterior_fluid - other_slice.v_exterior_fluid) > convergence_v) or \
               (abs(self.v_interior_fluid - other_slice.v_interior_fluid) > convergence_v)
            
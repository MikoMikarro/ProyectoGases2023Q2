import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline

# Define constants
length = 306.3 # cm
outter_diameter = 230.4 # cm
throat_diameter = 26.2 # cm
inner_diameter = 40 # cm

## Create a bezier curve for the nozzle
x = np.linspace(0, length, 30)
# bezier curve
x1 = np.array([0, 10, 20 , 40, 50, length-20 , length])
y1 = np.array([inner_diameter/2, inner_diameter/2, inner_diameter/2,  throat_diameter/2, \
                throat_diameter/2, outter_diameter/2,  outter_diameter/2])

spl1 = CubicSpline(x1, y1)

# Plot the nozzle
plt.plot(x, spl1(x), 'b-', lw=2, label='Nozzle')
plt.plot(x1, y1, 'ro', lw=2, label='Control Points')
plt.legend(loc='best')
plt.xlabel('Length (cm)')
plt.ylabel('Diameter (cm)')
plt.show()
import numpy as np
import matplotlib.pyplot as plt

#constants
c1 = 3.0e8        # wave speed in medium 1 (m/s)
c2 = 2.25e8       # wave speed in medium 2 (m/s)
h1 = 2.0          # height above interface (m)
h2 = 1.5          # depth below interface (m)
L  = 6.0          # horizontal distance between source and receiver projections (m)

#function for travel time
def travel_time(x):
    d1 = np.sqrt(x**2 + h1**2)            # path length in medium 1
    d2 = np.sqrt((L - x)**2 + h2**2)      # path length in medium 2
    return d1 / c1 + d2 / c2

#x range and find min
x_vals = np.linspace(0.0, L, 2000)
t_vals = travel_time(x_vals)
imin = np.argmin(t_vals)
x_min = x_vals[imin]
t_min = t_vals[imin]

#angles
sin_theta1 = x_min / np.sqrt(x_min**2 + h1**2)        # incidence
sin_theta2 = (L - x_min) / np.sqrt((L - x_min)**2 + h2**2)  # refraction

#snell's law
ratio_sin = sin_theta1 / sin_theta2
ratio_c   = c1 / c2
rel_error = (ratio_sin - ratio_c) / ratio_c

#results
print(f"Minimizing x = {x_min:.6f} m")
print(f"Minimum travel time = {t_min:.6e} s")
print(f"sin(theta1) = {sin_theta1:.8f}")
print(f"sin(theta2) = {sin_theta2:.8f}")
print(f"sin(theta1)/sin(theta2) = {ratio_sin:.8f}")
print(f"c1/c2 = {ratio_c:.8f}")
print(f"Relative error = {rel_error:.3e}")

#plot
plt.figure(figsize=(7,4))
plt.plot(x_vals, t_vals, label='t(x)')
plt.axvline(x_min, linestyle='--', color='r', label=f'Minimum at x = {x_min:.3f} m')
plt.scatter([x_min], [t_min], color='red', zorder=5)
plt.xlabel('x (m)')
plt.ylabel('Travel time t (s)')
plt.title('Travel time vs refraction point x')
plt.grid(True)
plt.legend()
plt.show()
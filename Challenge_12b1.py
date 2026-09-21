import numpy as np
import matplotlib.pyplot as plt

# Cauchy equation example (BK7 glass)
def refractive_index(lambda_um):
    A, B, C = 1.5046, 0.00420, 0.000042
    return A + B / (lambda_um**2) + C / (lambda_um**4)

# Parameters
alpha = np.deg2rad(45)  # prism apex angle
frequency = 542.5e12    # Hz
c = 3e8
wavelength_m = c / frequency
wavelength_um = wavelength_m * 1e6
n = refractive_index(wavelength_um)

theta_i_deg = np.linspace(0.1, 89.9, 500)  # avoid 0 and 90 deg
theta_i = np.deg2rad(theta_i_deg)

# Transmission angle using given equation
sin_theta_t = np.sqrt(n**2 - np.sin(theta_i)**2) * np.sin(alpha) - np.sin(theta_i) * np.cos(alpha)
theta_t = np.arcsin(sin_theta_t)

# Deflection angle
delta = theta_i + theta_t - alpha

# Plot θ_t vs θ_i
plt.figure()
plt.plot(theta_i_deg, np.rad2deg(theta_t))
plt.xlabel("Angle of incidence / deg")
plt.ylabel("Transmission angle θ_t / deg")
plt.title("Transmission vs incidence")
plt.grid(True)

# Plot δ vs θ_i
plt.figure()
plt.plot(theta_i_deg, np.rad2deg(delta))
plt.xlabel("Angle of incidence / deg")
plt.ylabel("Deflection angle δ / deg")
plt.title("Deflection vs incidence")
plt.grid(True)

plt.show()
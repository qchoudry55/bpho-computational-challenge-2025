import numpy as np
import matplotlib.pyplot as plt

#cauchy equation
def refractive_index(lambda_um):
    A, B, C = 1.5046, 0.00420, 0.000042
    return A + B / (lambda_um ** 2) + C / (lambda_um ** 4)

#constants
frequency = 542.5e12  # Hz
c = 3e8
wavelength_m = c / frequency
wavelength_um = wavelength_m * 1e6
n = refractive_index(wavelength_um)

#angles of incidence
theta_i_deg = np.linspace(0, 89.9, 500)  # avoid 0 and 90 deg
theta_i = np.deg2rad(theta_i_deg)

#prism apex angles in degrees (same as in your image)
alpha_list_deg = [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80]

plt.figure()
for alpha_deg in alpha_list_deg:
    alpha = np.deg2rad(alpha_deg)

    #transmission angle from given formula
    sin_theta_t = (np.sqrt(n ** 2 - np.sin(theta_i) ** 2) * np.sin(alpha)
                   - np.sin(theta_i) * np.cos(alpha))

    #only keep valid values where |sin_theta_t| <= 1
    valid_mask = np.abs(sin_theta_t) <= 1
    theta_t = np.full_like(theta_i, np.nan)
    theta_t[valid_mask] = np.arcsin(sin_theta_t[valid_mask])

    #deflection angle
    delta = theta_i + theta_t - alpha

    plt.plot(theta_i_deg, np.rad2deg(delta), label=f"α={alpha_deg}°")

plt.xlabel("Angle of incidence / deg")
plt.ylabel("Deflection angle δ / deg")
plt.title("Deflection angle vs incidence for various α")
plt.legend(ncol=2, fontsize=8)
plt.grid(True)
plt.show()
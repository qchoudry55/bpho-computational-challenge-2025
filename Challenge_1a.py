import numpy as np
import matplotlib.pyplot as plt

#sellmeier equation for BK7 crown glass
def sellmeier_crown_glass_n(lambda_um: np.ndarray) -> np.ndarray:
    #BK7 Sellmeier coefficients
    B1, B2, B3 = 1.03961212, 0.231792344, 1.01046945
    C1, C2, C3 = 0.00600069867, 0.0200179144, 103.560653
    lam2 = lambda_um**2
    n2 = 1 + (B1*lam2)/(lam2 - C1) + (B2*lam2)/(lam2 - C2) + (B3*lam2)/(lam2 - C3)
    return np.sqrt(n2)

#wavelength range (micrometers)
wavelengths_um = np.linspace(0.365, 1.1, 600)
n_vals = sellmeier_crown_glass_n(wavelengths_um)

#plot refractive index
plt.figure(figsize=(6,4))
plt.plot(wavelengths_um*1000, n_vals)  # convert μm to nm for x-axis
plt.xlabel("Wavelength (nm)")
plt.ylabel("Refractive index n")
plt.title("BK7 Crown Glass Refractive Index (Sellmeier Model)")
plt.grid(True)
plt.show()

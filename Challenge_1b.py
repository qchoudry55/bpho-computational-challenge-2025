import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

#function to compute refractive index of water
def water_refractive_index(f_THz):
    #convert to (f/10^15 Hz)^2
    f_scale = (np.array(f_THz) / 1000) ** 2
    term = 1.731 - 0.261 * f_scale
    return np.sqrt(1 + term ** (-1 / 2))

#map frequency in THz to RGB values and colour names
def frequency_to_rgb(f_THz):
    if 405 <= f_THz < 480:
        return (1.0, 0.0, 0.0), "Red"
    elif 480 <= f_THz < 510:
        return (1.0, 127 / 255, 0.0), "Orange"
    elif 510 <= f_THz < 530:
        return (1.0, 1.0, 0.0), "Yellow"
    elif 530 <= f_THz < 600:
        return (0.0, 1.0, 0.0), "Green"
    elif 600 <= f_THz < 620:
        return (0.0, 1.0, 1.0), "Cyan"
    elif 620 <= f_THz < 680:
        return (0.0, 0.0, 1.0), "Blue"
    elif 680 <= f_THz <= 790:
        return (127 / 255, 0.0, 1.0), "Violet"


#generate frequencies and refractive indices
frequencies_THz = np.linspace(405, 790, 500)
n_values = water_refractive_index(frequencies_THz)

#map frequencies to RGB colors
colors = [frequency_to_rgb(f)[0] for f in frequencies_THz]
color_names = [frequency_to_rgb(f)[1] for f in frequencies_THz]

#create a custom colourmap for the plot
cmap = LinearSegmentedColormap.from_list("visible_spectrum", colors, N=len(frequencies_THz))

#final plot parameters
plt.figure(figsize=(10, 6))
sc = plt.scatter(frequencies_THz, n_values, c=frequencies_THz, cmap=cmap, s=10)
plt.colorbar(sc, label="Frequency (THz) → Color")
plt.xlabel("Frequency (THz)")
plt.ylabel("Refractive Index (n)")
plt.title("Refractive Index of Water in the Visible Spectrum")
plt.grid(True)
plt.show()
import numpy as np
import matplotlib.pyplot as plt

#initial constants
L = 10.0
y1, y2 = 3.0, 3.0
c = 1.0

#function to find travel time
def travel_time(x):
    return (np.sqrt(x**2 + y1**2) + np.sqrt((L - x)**2 + y2**2)) / c

#define range of x values
x_values = np.linspace(0, L, 500)
t_values = travel_time(x_values)

#find minimum travel time
x_min = x_values[np.argmin(t_values)]
t_min = np.min(t_values)

#final plot parameters
plt.figure(figsize=(8, 5))
plt.plot(x_values, t_values, 'b-', label='Travel Time')
plt.axvline(x_min, color='r', linestyle='--', label=f'Min at x = {x_min:.1f} (L/2)')
plt.xlabel('Horizontal Position (x)')
plt.ylabel('Travel Time (t)')
plt.title('Travel Time vs Reflection Point Position')
plt.legend()
plt.grid(True)
plt.show()
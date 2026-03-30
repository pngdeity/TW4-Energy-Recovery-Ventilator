import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import json
def load_coordinates(filename):
    with open(filename, 'r') as json_file:
        coordinates = json.load(json_file)
    return coordinates

def extract_elements(array_2d, element):
    # Ensure the input is a 2D NumPy array
    if array_2d.ndim != 2:
        raise ValueError("Input must be a 2D NumPy array")
    
    # Extract the first element from each row
    first_elements = array_2d[:, element]
    
    return first_elements

samples = load_coordinates('raw_data.json')
array1 = np.array(samples) # convert list to array

# Flatten the arrays for plotting 
x_flat = extract_elements(array1, 0)
y_flat = extract_elements(array1, 1)
z_flat = extract_elements(array1, 2)

# Create a figure and 3D axis
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot a 3D scatter plot
sc = ax.scatter(x_flat, y_flat, z_flat, c=z_flat, cmap='viridis', marker='o')

# Add a color bar
plt.colorbar(sc, ax=ax, shrink=0.5, aspect=5)

# Set labels
ax.set_xlabel('throttle')
ax.set_ylabel('rpm')
ax.set_zlabel('anem')

# Show the plot
plt.show()

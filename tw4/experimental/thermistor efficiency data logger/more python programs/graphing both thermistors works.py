import numpy as np
import matplotlib.pyplot as plt
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

samples = load_coordinates('samplescombined.json')
samplest1 = []
for i in samples:
    samplest1.append([i[0], i[2]])
samplest2 = []
for i in samples:
    samplest2.append([i[1], i[2]])

array1 = np.array(samplest1)  # Convert list to array
array2 = np.array(samplest2)  # Convert samplest2 to array

# Flatten the arrays for plotting
x_flat1 = extract_elements(array1, 0)
z_flat1 = extract_elements(array1, 1)

x_flat2 = extract_elements(array2, 0)
z_flat2 = extract_elements(array2, 1)

# Create a figure
fig, ax = plt.subplots()

# Plot both samplest1 and samplest2 on the same graph
ax.plot(z_flat1, x_flat1, label='Data from samplest1', color='b')  # Line for samplest1
ax.plot(z_flat2, x_flat2,  label='Data from samplest2', color='r')  # Line for samplest2

# Add labels and title
ax.set_xlabel('ms clock')
ax.set_ylabel('temperature')
ax.set_title('Temperature vs ms timestamp')

# Show the legend
plt.legend()

# Show the plot
plt.show()

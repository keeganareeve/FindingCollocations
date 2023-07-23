'''
Graphs the first column from output.txt (the frequencies of the words) and fits it to the power law.
'''

import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Replace 'your_file.txt' with the path to your text file
file_path = str(sys.argv[1])

# Step 2: Define the power-law function


def power_law(x, a, b):
    return a * np.power(x, b)


def extract_first_word(file_path):
    first_words_list = []
    with open(file_path, 'r') as file:
        for line in file:
            # Split the line by whitespace and get the first word
            first_word = line.strip().split()[0]
            first_words_list.append(first_word)
    return first_words_list


frequency_number_list = extract_first_word(file_path)
index_number_range = range(0, len(frequency_number_list))
index_number_list = list(index_number_range)

# Step 3: Load or create your dataset (x and y arrays)
# Example dataset
x = np.array(index_number_list)
y = np.array(frequency_number_list)

# Step 4: Use curve_fit to fit the data to the power law function
params, covariance = curve_fit(power_law, x, y)

# Step 5: Plot the original data and the fitted curve
x_fit = np.linspace(min(x), max(x), 100)
y_fit = power_law(x_fit, params[0], params[1])

plt.scatter(x, y, label='Original Data')
plt.plot(x_fit, y_fit, 'r-', label='Fitted Power Law Curve')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.title('Power Law Fit')
plt.grid(True)
plt.show()

# The parameters 'params' will contain the fitted values of 'a' and 'b'.
fitted_a, fitted_b = params
print(f"Fitted parameters: a = {fitted_a}, b = {fitted_b}")

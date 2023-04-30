import numpy as np
from scipy.optimize import least_squares

# Define the model function to be optimized
def gaussian_mixture(params, x):
    n = len(params) // 3
    weights = params[:n]
    means = params[n:2*n]
    stds = params[2*n:]
    components = np.array([weights[i] * np.exp(-0.5 * ((x - means[i]) / stds[i])**2)
                           for i in range(n)])
    return components.sum(axis=0)

# Define the objective function to be minimized
def objective(params, x, y):
    return gaussian_mixture(params, x) - y

# Generate some example data
x = np.linspace(0, 10, 1000)
y_true = 0.3 * np.exp(-0.5 * ((x - 3) / 1)**2) + 0.7 * np.exp(-0.5 * ((x - 7) / 0.5)**2)
y_noisy = y_true + 0.05 * np.random.randn(len(x))

# Initialize the parameters
n_components = 2
weights = np.ones(n_components) / n_components
means = np.linspace(1, 9, n_components)
stds = np.ones(n_components)

params0 = np.concatenate([weights, means, stds])

# Use the Levenberg-Marquardt algorithm to optimize the parameters
result = least_squares(objective, params0, args=(x, y_noisy), method='lm')

# Extract the optimal parameters
optimal_params = result.x
optimal_weights = optimal_params[:n_components]
optimal_means = optimal_params[n_components:2*n_components]
optimal_stds = optimal_params[2*n_components:]

# Evaluate the optimal Gaussian mixture model on the data
y_optimal = gaussian_mixture(optimal_params, x)

# Plot the results
import matplotlib.pyplot as plt
plt.plot(x, y_noisy, label='Noisy data')
plt.plot(x, y_true, label='True signal')
plt.plot(x, y_optimal, label='Optimal model')
plt.legend()
plt.show()

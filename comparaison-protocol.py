import numpy as np
import matplotlib.pyplot as plt


simulation_1_data = np.load("./Results/simulation_static_results.npz")['call_rejections']
simulation_2_data = np.load("./Results/simulation_load_balancing_results.npz")['call_rejections']
simulation_3_data = np.load("./Results/simulation_adaptatif_results.npz")['call_rejections']

# Plot des résultats
plt.figure(figsize=(10, 6))

# Simulation 1
plt.plot(simulation_1_data[:, 0], simulation_1_data[:, 1], label="Routage Statique", color="crimson", linewidth=2)

# Simulation 2
plt.plot(simulation_2_data[:, 0], simulation_2_data[:, 1], label="Partage de charge", color="blue", linewidth=2)

# Simulation 3
plt.plot(simulation_3_data[:, 0], simulation_3_data[:, 1], label="Routage adaptatif", color="green", linewidth=2)

# Configuration des axes
plt.xlabel("Total Attempted Calls")
plt.ylabel("Number of Rejected Calls")
plt.title("Rejected Calls vs. Attempted Calls for Three Simulations")
# plt.ylim(0, 150) 
# plt.xlim(0, 150)  
plt.legend()
plt.grid(True)
plt.show()

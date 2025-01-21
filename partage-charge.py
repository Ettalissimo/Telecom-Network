import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Simulation parameters
num_phones = 10  # Number of phones per station
simulation_duration = 10 * 60  # Total simulation time (seconds)
max_call_duration = 5 * 60  # Maximum call duration (seconds)

# Link capacities
link_CA1_CA2 = 10
link_CA2_CA3 = 10

link_CA1_CTS1 = 100
link_CA1_CTS2 = 100
link_CA2_CTS1 = 100
link_CA2_CTS2 = 100
link_CA3_CTS1 = 100
link_CA3_CTS2 = 100

link_CTS1_CTS2 = 1000

# Initialize variables
failed_calls = 0  # Number of failed calls
successful_calls = 0  # Number of successful calls
total_attempted_calls = 0  # Total number of attempted calls
call_rejections_over_time = []
ongoing_calls = np.zeros((130, 3), dtype=int)  # Ongoing calls (duration tracking)

def record_statistics():
    """Record call statistics for analysis."""
    call_rejections_over_time.append((total_attempted_calls, failed_calls))

time_step = 0  # Time step (seconds)
call_probability = 0.2  # Probability of a call being made
while time_step < simulation_duration:
    # Generate new calls
    new_calls = np.random.rand(3) < call_probability
    total_attempted_calls += np.sum(new_calls)

    # Call handling: CA1 <-> CA2
    if new_calls[0]:
        if link_CA1_CA2 == 0:
            failed_calls += 1
        else:
            successful_calls += 1
            link_CA1_CA2 -= 1
            empty_slot = np.where(ongoing_calls[:, 0] == 0)[0]
            ongoing_calls[empty_slot[0], 0] = np.random.randint(1, max_call_duration + 1)

    # Call handling: CA2 <-> CA3
    if new_calls[1]:
        if link_CA2_CA3 == 0:
            failed_calls += 1
        else:
            successful_calls += 1
            link_CA2_CA3 -= 1
            empty_slot = np.where(ongoing_calls[:, 1] == 0)[0]
            ongoing_calls[empty_slot[0], 1] = np.random.randint(1, max_call_duration + 1)

    # Call handling: CA1 <-> CA3 via CTS1
    if new_calls[2]:
        if link_CA1_CTS1 == 0 or link_CA3_CTS1 == 0:
            failed_calls += 1
        else:
            successful_calls += 1
            link_CA1_CTS1 -= 1
            link_CA3_CTS1 -= 1
            empty_slot = np.where(ongoing_calls[:, 2] == 0)[0]
            ongoing_calls[empty_slot[0], 2] = np.random.randint(1, max_call_duration + 1)

    # Release completed calls and free resources
    calls_ending_CA1_CA2 = np.sum(ongoing_calls[:, 0] == 1)
    link_CA1_CA2 += calls_ending_CA1_CA2

    calls_ending_CA2_CA3 = np.sum(ongoing_calls[:, 1] == 1)
    link_CA2_CA3 += calls_ending_CA2_CA3

    calls_ending_CA1_CA3 = np.sum(ongoing_calls[:, 2] == 1)
    link_CA1_CTS1 += calls_ending_CA1_CA3
    link_CA3_CTS1 += calls_ending_CA1_CA3

    # Decrease remaining call durations and increment time step
    time_step += 1
    ongoing_calls[ongoing_calls > 0] -= 1

    # Record statistics
    record_statistics()

    # Sauvegarder les résultats dans un fichier
np.savez("simulation_2_results.npz", call_rejections=np.array(call_rejections_over_time))

# Calculate success rate
success_rate = 100 * successful_calls / (failed_calls + successful_calls)
print(f"Call success rate: {success_rate:.2f}%")

# Network adjacency matrix
adjacency_matrix = np.array([
    [0, link_CTS1_CTS2, link_CA1_CTS1, link_CA2_CTS1, link_CA3_CTS1],
    [link_CTS1_CTS2, 0, link_CA1_CTS2, link_CA2_CTS2, link_CA3_CTS2],
    [link_CA1_CTS1, link_CA1_CTS2, 0, link_CA1_CA2, 0],
    [link_CA2_CTS1, link_CA2_CTS2, link_CA1_CA2, 0, link_CA2_CA3],
    [link_CA3_CTS1, link_CA3_CTS2, 0, link_CA2_CA3, 0]
])

# Create and display the network graph
station_names = ['CTS1', 'CTS2', 'CA1', 'CA2', 'CA3']
network_graph = nx.from_numpy_array(adjacency_matrix, create_using=nx.DiGraph)

positions = {
    0: [-0.5, 1],
    1: [0.5, 1],
    2: [-1, -0.5],
    3: [0, -1],
    4: [1, -0.5]
}

plt.figure(figsize=(9, 7))
nx.draw(network_graph, positions, with_labels=True, labels={i: station_names[i] for i in range(len(station_names))}, node_size=1700, node_color="lightblue")
edge_labels = nx.get_edge_attributes(network_graph, 'weight')
nx.draw_networkx_edge_labels(network_graph, positions, edge_labels={(u, v): adjacency_matrix[u][v] for u, v in network_graph.edges()})

plt.title("Telecommunication Network Graph")

# Plot rejected calls over time
call_rejections_over_time = np.array(call_rejections_over_time)
plt.figure(figsize=(10, 6))
plt.plot(call_rejections_over_time[:, 0], call_rejections_over_time[:, 1], label="Rejected Calls", color="crimson", linewidth=2)
plt.xlabel("Total Attempted Calls")
plt.ylabel("Number of Rejected Calls")
plt.title("Rejected Calls vs. Attempted Calls")
plt.ylim(0, 150)  # Set y-axis limit to a maximum of 150
plt.legend()
plt.grid(True)
#plt.show()

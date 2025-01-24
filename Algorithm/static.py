import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


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

link_U1_CA1 = 1000
link_U2_CA2 = 1000
link_U3_CA3 = 1000


# Simulation parameters
simulation_duration = 10 * 60  # Total simulation time (seconds)
max_call_duration = 5 * 60  # Maximum call duration (seconds)


failed_calls = 0                # Number of failed calls
successful_calls = 0            # Number of successful calls
total_attempted_calls = 0       # Total number of attempted calls
call_rejections = []            # list of rejected calls

nbr_slots = 130
ongoing_calls = np.zeros((nbr_slots, 4), dtype=int)  

time_step = 0  # Time step 
call_probability = 0.2  # Probability of a call being made



def record_statistics():
    """Record call statistics for analysis."""
    call_rejections.append((total_attempted_calls, failed_calls))



while time_step < simulation_duration:
    # Generate new calls
    new_calls = np.random.rand(4) < call_probability
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

    # Call handling: CA1 <-> CA3 via CTS2
    if new_calls[3]:
        if link_CA1_CTS2 == 0 or link_CA3_CTS2 == 0:
            failed_calls += 1
        else:
            successful_calls += 1
            link_CA1_CTS2 -= 1
            link_CA3_CTS2 -= 1
            empty_slot = np.where(ongoing_calls[:, 3] == 0)[0]
            ongoing_calls[empty_slot[0], 3] = np.random.randint(1, max_call_duration + 1)


    # Release completed calls and free resources
    calls_ending_CA1_CA2 = np.sum(ongoing_calls[:, 0] == 1)
    link_CA1_CA2 += calls_ending_CA1_CA2

    calls_ending_CA2_CA3 = np.sum(ongoing_calls[:, 1] == 1)
    link_CA2_CA3 += calls_ending_CA2_CA3

    calls_ending_CA1_CA3 = np.sum(ongoing_calls[:, 2] == 1)
    link_CA1_CTS1 += calls_ending_CA1_CA3
    link_CA3_CTS1 += calls_ending_CA1_CA3

    calls_ending_CA1_CA3 = np.sum(ongoing_calls[:, 3] == 1)
    link_CA1_CTS2 += calls_ending_CA1_CA3
    link_CA3_CTS2 += calls_ending_CA1_CA3

    # Decrease remaining call durations and increment time step
    time_step += 1
    ongoing_calls[ongoing_calls > 0] -= 1

    # Record statistics
    record_statistics()


# Sauvegarder les résultats dans un fichier
np.savez("./Results/simulation_static_results.npz", call_rejections=np.array(call_rejections))

# Calculate success rate
success_rate = 100 * successful_calls / (failed_calls + successful_calls)
print(f"Call success rate: {success_rate:.2f}%")

import numpy as np
import matplotlib.pyplot as plt


# Parameters
num_phones = 10  # Number of phones per station
simulation_duration = 10 * 60  # Total simulation time (seconds)
max_call_duration = 5 * 60  # Maximum call duration (seconds)

# Initial capacities
link_CA1_CA2 = 10
link_CA1_CTS1 = 100
link_CA1_CTS2 = 100

# Initialize variables
failed_calls = 0  # Number of failed calls
successful_calls = 0  # Number of successful calls
total_attempted_calls = 0  # Total number of attempted calls
call_rejections = []
ongoing_calls = np.zeros((130, 3), dtype=int)  # Ongoing calls (duration tracking)

def record_statistics():
    """Record call statistics for analysis."""
    call_rejections.append((total_attempted_calls, failed_calls))

time_step = 0  # Time step (seconds)
call_probability = 0.2  # Probability of a call being made
while time_step < simulation_duration:
    # Generate new calls
    new_calls = np.random.rand(3) < call_probability
    total_attempted_calls += np.sum(new_calls)

    # Handle new calls from CA1
    for new_call in new_calls:
        if new_call:
            # Adaptive routing: calculate available capacities
            total_capacity = link_CA1_CA2 + link_CA1_CTS1 + link_CA1_CTS2
            if total_capacity == 0:  # All links are saturated
                failed_calls += 1
                continue

            # Calculate probabilities proportional to remaining capacities
            prob_CA2 = link_CA1_CA2 / total_capacity if link_CA1_CA2 > 0 else 0
            prob_CTS1 = link_CA1_CTS1 / total_capacity if link_CA1_CTS1 > 0 else 0
            prob_CTS2 = link_CA1_CTS2 / total_capacity if link_CA1_CTS2 > 0 else 0
            probabilities = [prob_CA2, prob_CTS1, prob_CTS2]

            # Choose route based on probabilities
            route = np.random.choice(["CA2", "CTS1", "CTS2"], p=probabilities)
            
            if route == "CA2":
                # CA1 <-> CA2
                if link_CA1_CA2 > 0:
                    successful_calls += 1
                    link_CA1_CA2 -= 1
                    empty_slot = np.where(ongoing_calls[:, 0] == 0)[0]
                    ongoing_calls[empty_slot[0], 0] = np.random.randint(1, max_call_duration + 1)
                else:
                    failed_calls += 1
            elif route == "CTS1":
                # CA1 <-> CTS1
                if link_CA1_CTS1 > 0:
                    successful_calls += 1
                    link_CA1_CTS1 -= 1
                    empty_slot = np.where(ongoing_calls[:, 1] == 0)[0]
                    ongoing_calls[empty_slot[0], 1] = np.random.randint(1, max_call_duration + 1)
                else:
                    failed_calls += 1
            elif route == "CTS2":
                # CA1 <-> CTS2
                if link_CA1_CTS2 > 0:
                    successful_calls += 1
                    link_CA1_CTS2 -= 1
                    empty_slot = np.where(ongoing_calls[:, 2] == 0)[0]
                    ongoing_calls[empty_slot[0], 2] = np.random.randint(1, max_call_duration + 1)
                else:
                    failed_calls += 1

    # Release completed calls and free resources
    calls_ending_CA1_CA2 = np.sum(ongoing_calls[:, 0] == 1)
    link_CA1_CA2 += calls_ending_CA1_CA2

    calls_ending_CA1_CTS1 = np.sum(ongoing_calls[:, 1] == 1)
    link_CA1_CTS1 += calls_ending_CA1_CTS1

    calls_ending_CA1_CTS2 = np.sum(ongoing_calls[:, 2] == 1)
    link_CA1_CTS2 += calls_ending_CA1_CTS2

    # Decrease remaining call durations and increment time step
    time_step += 1
    ongoing_calls[ongoing_calls > 0] -= 1

    # Record statistics
    record_statistics()

# Output results
print(f"Total attempted calls: {total_attempted_calls}")
print(f"Successful calls: {successful_calls}")
print(f"Failed calls: {failed_calls}")

# Sauvegarder les résultats dans un fichier
np.savez("./Results/simulation_adaptatif_results.npz", call_rejections=np.array(call_rejections))

# Calculate success rate
success_rate = 100 * successful_calls / (failed_calls + successful_calls)
print(f"Call success rate: {success_rate:.2f}%")


# Plot rejected calls over time
call_rejections_over_time = np.array(call_rejections)
plt.figure(figsize=(10, 6))
plt.plot(call_rejections_over_time[:, 0], call_rejections_over_time[:, 1], label="Rejected Calls", color="crimson", linewidth=2)
plt.xlabel("Total Attempted Calls")
plt.ylabel("Number of Rejected Calls")
plt.title("Rejected Calls vs. Attempted Calls")
plt.ylim(0, 150)  # Set y-axis limit to a maximum of 150
plt.legend()
plt.grid(True)
# plt.show()
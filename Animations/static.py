import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import networkx as nx

# Définir les capacités des liens
capacities = {
    "CA1_CA2": 10,
    "CA2_CA3": 10,
    "CA1_CTS1": 100,
    "CA1_CTS2": 100,
    "CA2_CTS1": 100,
    "CA2_CTS2": 100,
    "CA3_CTS1": 100,
    "CA3_CTS2": 100,
    "CTS1_CTS2": 1000,
    "U1_CA1": 1000,
    "U2_CA2": 1000,
    "U3_CA3": 1000,
}

# Durée totale de la simulation
simulation_duration = 300  # 5 minutes
call_probability = 0.2  # Probabilité qu'un appel soit généré à chaque étape

# Variables pour les statistiques
failed_calls = 0
successful_calls = 0
total_attempted_calls = 0

# Créer un graphe avec NetworkX
G = nx.DiGraph()

# Ajouter les nœuds
nodes = ["U1", "CA1", "U2", "CA2", "U3", "CA3", "CTS1", "CTS2"]
G.add_nodes_from(nodes)

# Ajouter les liens (edges) avec leurs capacités
edges = [
    ("U1", "CA1"), ("U2", "CA2"), ("U3", "CA3"),
    ("CA1", "CA2"), ("CA2", "CA3"),
    ("CA1", "CTS1"), ("CA1", "CTS2"),
    ("CA2", "CTS1"), ("CA2", "CTS2"),
    ("CA3", "CTS1"), ("CA3", "CTS2"),
    ("CTS1", "CTS2")
]
G.add_edges_from(edges)

# Ajouter des positions pour un affichage clair
positions = {
    "U1": (1, 2), "CA1": (2, 2),
    "U2": (0, 1), "CA2": (1, 1),
    "U3": (1, 0), "CA3": (2, 0),
    "CTS1": (3, 0.5), "CTS2": (3, 1.5),
}

# Préparer l'affichage
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_title("Simulation de routage des appels", fontsize=14)

# Créer les couleurs initiales des liens
edge_colors = {edge: "black" for edge in edges}

def update(frame):
    global failed_calls, successful_calls, total_attempted_calls, capacities

    ax.clear()
    ax.set_title("Simulation de routage des appels", fontsize=14)

    # Générer de nouveaux appels
    new_calls = np.random.rand(len(nodes) // 2) < call_probability
    total_attempted_calls += np.sum(new_calls)

    for idx, call in enumerate(new_calls):
        if call:  # Si un appel est généré
            if idx == 0:  # U1 -> CA1 -> CA2
                path = ["U1", "CA1", "CA2"]
                if capacities["CA1_CA2"] > 0:
                    successful_calls += 1
                    capacities["CA1_CA2"] -= 1
                    edge_colors[("CA1", "CA2")] = "green"
                else:
                    failed_calls += 1
                    edge_colors[("CA1", "CA2")] = "red"

            elif idx == 1:  # U2 -> CA2 -> CA3
                path = ["U2", "CA2", "CA3"]
                if capacities["CA2_CA3"] > 0:
                    successful_calls += 1
                    capacities["CA2_CA3"] -= 1
                    edge_colors[("CA2", "CA3")] = "green"
                else:
                    failed_calls += 1
                    edge_colors[("CA2", "CA3")] = "red"

            elif idx == 2:  # U3 -> CA3 -> CTS1
                path = ["U3", "CA3", "CTS1"]
                if capacities["CA3_CTS1"] > 0:
                    successful_calls += 1
                    capacities["CA3_CTS1"] -= 1
                    edge_colors[("CA3", "CTS1")] = "green"
                else:
                    failed_calls += 1
                    edge_colors[("CA3", "CTS1")] = "red"

            else:  # U1 -> CA1 -> CTS2
                path = ["U1", "CA1", "CTS2"]
                if capacities["CA1_CTS2"] > 0:
                    successful_calls += 1
                    capacities["CA1_CTS2"] -= 1
                    edge_colors[("CA1", "CTS2")] = "green"
                else:
                    failed_calls += 1
                    edge_colors[("CA1", "CTS2")] = "red"

    # Réinitialiser les couleurs pour l'étape suivante
    for edge in edge_colors.keys():
        if edge_colors[edge] != "black":
            edge_colors[edge] = "black"

    # Dessiner les nœuds et les liens
    nx.draw_networkx_nodes(G, positions, ax=ax, node_size=700, node_color="skyblue")
    nx.draw_networkx_labels(G, positions, ax=ax, font_size=10, font_color="black")
    nx.draw_networkx_edges(G, positions, ax=ax, edge_color=[edge_colors[edge] for edge in G.edges], width=2)

    # Afficher les statistiques
    ax.text(0.05, 0.95, f"Appels réussis: {successful_calls}", transform=ax.transAxes, fontsize=10, color="green")
    ax.text(0.05, 0.90, f"Appels échoués: {failed_calls}", transform=ax.transAxes, fontsize=10, color="red")
    ax.text(0.05, 0.85, f"Appels totaux: {total_attempted_calls}", transform=ax.transAxes, fontsize=10, color="black")


# Créer l'animation
ani = animation.FuncAnimation(fig, update, frames=simulation_duration, interval=100, repeat=False)

# Afficher l'animation
plt.show()

import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import random
import json
import os

# ========== LOGIQUE ==========
def generate_graph(num_nodes, connection_prob):
    return nx.erdos_renyi_graph(num_nodes, connection_prob, seed=random.randint(0, 1000))

def simulate_coloring(graph):
    colors = {}
    for node in graph.nodes:
        colors[node] = random.randint(0, 5)  # Fréquences de 0 à 5
    return colors

def plot_graph(graph, colors):
    pos = nx.spring_layout(graph)
    node_colors = [colors[node] for node in graph.nodes]

    fig, ax = plt.subplots(figsize=(10, 8))
    nx.draw(graph, pos, with_labels=True, node_color=node_colors, cmap=plt.cm.Set3, edge_color='gray', ax=ax)
    ax.set_title("Coloration simulée (Fréquences radio)")
    return fig

def export_frequencies_to_json(colors, filename):
    with open(filename, 'w') as f:
        json.dump(colors, f, indent=4)

# ========== INTERFACE STREAMLIT ==========
st.set_page_config(page_title="Attribution de Fréquences Radio", layout="wide")
st.title("📡 Simulation d'Attribution de Fréquences Radio par Coloration de Graphe")

st.sidebar.header("🔧 Paramètres du Graphe")
num_nodes = st.sidebar.slider("Nombre de stations (nœuds)", 5, 50, 20)
connection_prob = st.sidebar.slider("Probabilité de connexion", 0.0, 1.0, 0.3, step=0.05)

if st.sidebar.button("🎲 Générer le graphe"):
    G = generate_graph(num_nodes, connection_prob)
    frequencies = simulate_coloring(G)

    # Affichage du graphe
    st.subheader("🖼️ Graphe coloré")
    fig = plot_graph(G, frequencies)
    st.pyplot(fig)

    # Export JSON
    os.makedirs("output", exist_ok=True)
    json_path = f"output/frequences_{num_nodes}noeuds.json"
    export_frequencies_to_json(frequencies, json_path)
    st.success(f"Fréquences exportées dans : {json_path}")

    st.download_button("📥 Télécharger les fréquences (JSON)", data=json.dumps(frequencies, indent=4), file_name="frequences.json", mime="application/json")

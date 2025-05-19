import json
import networkx as nx
import matplotlib.pyplot as plt

# Load data
file_path = "filtered_prs.json"
with open(file_path, "r") as f:
    prs = json.load(f)

# Create a directed graph
G = nx.DiGraph()

# Add nodes and edges
for pr in prs:
    author = pr["user"]
    commenters = pr["commenters"]
    
    G.add_node(author)  # Ensure the author is in the graph
    
    for commenter in commenters:
        G.add_node(commenter)
        if commenter != author:
            G.add_edge(author, commenter)  # Add edge from author to commenter

'''# Compute node influence (degree)
node_degrees = dict(G.degree())  # Get degree of each node
top_nodes = sorted(node_degrees, key=node_degrees.get, reverse=True)[:20]  # Top nodes

# Create a subgraph with only top 100 influential nodes
G_top = G.subgraph(top_nodes).copy()

# Draw the graph
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, seed=42)  # Layout for better readability
nx.draw(G_top, pos, with_labels=True, node_color="lightblue", edge_color="gray", node_size=2000, font_size=10)
plt.title("Bitcoin BIP Interaction Network")
plt.show()'''

'''# Compute betweenness centrality
betweenness_scores = nx.betweenness_centrality(G)

# Select top 100 influential nodes by betweenness
top_nodes = sorted(betweenness_scores, key=betweenness_scores.get, reverse=True)[:100]

# Create a subgraph with only the top 100
G_top = G.subgraph(top_nodes).copy()

# Scale node size for visualization
node_sizes = [betweenness_scores[node] * 5000 for node in G_top.nodes()]

# Draw the graph
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G_top, seed=42)  # Layout for better readability
nx.draw(G_top, pos, with_labels=True, node_color="lightcoral", edge_color="gray",
        node_size=node_sizes, font_size=10, alpha=0.8)
plt.title("Top 100 Influential GitHub Users (Betweenness Centrality)")
plt.show()'''

# Compute PageRank
pagerank_scores = nx.pagerank(G, alpha=0.85)  # Higher alpha means longer influence propagation

# Select top 100 nodes by PageRank
top_nodes = sorted(pagerank_scores, key=pagerank_scores.get, reverse=True)[:20]

# Create a subgraph with the top 100 influential nodes
G_top = G.subgraph(top_nodes).copy()

# Get PageRank scores for visualization (scale for better visibility)
node_sizes = [pagerank_scores[node] * 5000 for node in G_top.nodes()]  # Scale factor for clarity

# Draw the graph
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G_top, seed=42)  # Layout for readability
nx.draw(G_top, pos, with_labels=True, node_color="lightblue", edge_color="gray",
        node_size=node_sizes, font_size=10, alpha=0.8)
plt.title("Top 100 Influential GitHub Users (PageRank-Based)")
plt.show()

import csv

output_csv = "pagerank_top_100.csv"

# Sort users by PageRank
top_users = sorted(pagerank_scores.items(), key=lambda x: x[1], reverse=True)[:100]

# Save to CSV
with open(output_csv, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["User", "PageRank Score"])
    writer.writerows(top_users)

print(f"Top 100 users exported to {output_csv}")


'''from pyvis.network import Network

# Create Pyvis network visualization
net = Network(notebook=False, directed=True)
for node in G_top.nodes():
    net.add_node(node, size=pagerank_scores[node] * 50, title=f"PageRank: {pagerank_scores[node]:.4f}")

for source, target in G_top.edges():
    net.add_edge(source, target)

# Save as interactive HTML file
output_file = "github_pr_network.html"
net.show(output_file)

print(f"Interactive network saved as {output_file}")

'''
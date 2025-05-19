import json
import networkx as nx
import matplotlib.pyplot as plt
import csv

# Load data
file_path = "filtered_prs_ETC.json"
with open(file_path, "r") as f:
    prs = json.load(f)

# Create a directed graph
G = nx.DiGraph()

# Add nodes and edges
for pr in prs:
    author = pr["user"]
    commenters = pr["commenters"]
    reviewers = pr["reviewers"]
    
    G.add_node(author)  # Ensure the author is in the graph
    
    for commenter in commenters:
        G.add_node(commenter)
        if commenter != author:
            G.add_edge(commenter, author)  # Add edge from author to commenter
    
    for reviewer in reviewers:
        G.add_node(reviewer)
        if reviewer != author:
            G.add_edge(reviewer, author, weight = 5)  # Add edge from author to reviewer
#Exclude known bots
try: 
    G.remove_node("eth-bot") 
except nx.exception.NetworkXError:
    print("")
try: 
    G.remove_node("dependabot[bot]") 
except nx.exception.NetworkXError:
    print("")
try: 
    G.remove_node("renovate[bot]") 
except nx.exception.NetworkXError:
    print("")
try: 
    G.remove_node("github-actions[bot]") 
except nx.exception.NetworkXError:
    print("")
try: 
    G.remove_node("eip-automerger") 
except nx.exception.NetworkXError:
    print("")
betweenness_scores = nx.betweenness_centrality(G)
degree_scores = dict(nx.degree(G))  # Get degree of each node

# Sort users by degree (highest first)
top_users = sorted(degree_scores.items(), key=lambda x: x[1], reverse=True)  # Optional: add [:100] to limit

# Output file
output1_csv = "degreesETC.csv"

# Save to CSV
with open(output1_csv, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["User", "Degree Score"])
    writer.writerows(top_users)

print(f"Degree scores exported to {output1_csv}")
# Create a subgraph with only top influential nodes
top_users = sorted(degree_scores.items(), key=lambda x: x[1], reverse=True)[:100]
top_nodes = [user for user, _ in top_users]
G_top = G.subgraph(top_nodes).copy()


# Draw the graph
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G_top, seed=42)  # Layout for better readability
nx.draw(G_top, pos, with_labels=False, node_color="lightblue", edge_color="gray", node_size=200, font_size=10)
plt.title("Bitcoin IP Interaction Network Top 100 by Degree")
plt.show()

# Compute betweenness centrality

# Select top 100 influential nodes by betweenness
#top_nodes = sorted(betweenness_scores, key=betweenness_scores.get, reverse=True)[:100]

# Create a subgraph with only the top 100
#G_top = G.subgraph(top_nodes).copy()

# Scale node size for visualization
#node_sizes = [betweenness_scores[node] * 5000 for node in G_top.nodes()]

'''
# Draw the graph
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G_top, seed=42)  # Layout for better readability
nx.draw(G_top, pos, with_labels=True, node_color="lightcoral", edge_color="gray",
        node_size=node_sizes, font_size=10, alpha=0.8)
plt.title("Top 100 Influential GitHub Users (Betweenness Centrality)")
plt.show()
'''

output_csv = "betweennessETC2.csv"

# Sort users
top_users_b = sorted(betweenness_scores.items(), key=lambda x: x[1], reverse=True)#[:100]

# Save to CSV
with open(output_csv, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["User", "Betweenness Score"])
    writer.writerows(top_users_b)

print(f"Betweenness values exported to {output_csv}")


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
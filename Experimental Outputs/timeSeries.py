import pandas as pd
import json
import networkx as nx
from itertools import combinations
import numpy as np
import matplotlib.pyplot as plt

# If the data is stored in a file:
with open('filtered_prs_ETC.json', 'r') as file:
    data = json.load(file)

df = pd.DataFrame(data)

df['created_at'] = pd.to_datetime(df['created_at'], utc=True)
df['closed_at'] = pd.to_datetime(df['closed_at'], utc=True, errors='coerce')

df.set_index('created_at', inplace=True)
df.sort_index(inplace=True)

monthly_groups = df.groupby(pd.Grouper(freq='M'))

monthly_graphs = {}

for month, group in monthly_groups:
    G = nx.Graph()
    
    for _, pr in group.iterrows():
        participants = set([pr['user']] + pr['reviewers'] + pr['commenters'])
        
        # Add nodes (users, reviewers, commenters)
        G.add_nodes_from(participants)
        
        # Create edges (all combinations among participants)
        edges = combinations(participants, 2)
        G.add_edges_from(edges)
    
    monthly_graphs[month] = G

monthly_centralities = {}
try: 
    G.remove_node("eth-bot") 
except nx.exception.NetworkXError:
    print("no eth")
try: 
    G.remove_node("dependabot[bot]") 
except nx.exception.NetworkXError:
    print("no dep")
try: 
    G.remove_node("renovate[bot]") 
except nx.exception.NetworkXError:
    print("no ren")
try: 
    G.remove_node("github-actions[bot]") 
except nx.exception.NetworkXError:
    print("no git-ac")
try: 
    G.remove_node("eip-automerger") 
except nx.exception.NetworkXError:
    print("no eip")

for month, G in monthly_graphs.items():
    centrality = nx.betweenness_centrality(G)
    monthly_centralities[month] = centrality

'''def gini(values):
    sorted_vals = np.sort(values)
    n = len(values)
    cumulative = np.cumsum(sorted_vals)
    numerator = np.sum((np.arange(1, n+1) - 0.5) * sorted_vals)
    denominator = cumulative[-1] * n
    return 1 - (2 * numerator) / denominator if denominator else 0'''

def gini(x):
    total = 0
    x = np.array(x)
    for i, xi in enumerate(x[:-1], 1):
        total += np.sum(np.abs(xi - x[i:]))
    return total / (len(x)**2 * np.mean(x))

monthly_gini = {}

for month, centrality_dict in monthly_centralities.items():
    centrality_values = list(centrality_dict.values())
    monthly_gini[month] = gini(centrality_values)

result_df = pd.DataFrame({
    'month': list(monthly_centralities.keys()),
    'gini_coefficient': list(monthly_gini.values()),
})

# Example betweenness centrality for top nodes each month:
result_df['top_5_nodes'] = [
    sorted(c.items(), key=lambda x: x[1], reverse=True)[:5] for c in monthly_centralities.values()
]

print(result_df)

result_df.set_index('month', inplace=True)

plt.figure(figsize=(12,6))
plt.plot(result_df.index, result_df['gini_coefficient'], marker='o', linestyle='-')
plt.title('Monthly Gini Coefficient for Betweenness Centrality')
plt.ylabel('Gini Coefficient')
plt.xlabel('Month')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()
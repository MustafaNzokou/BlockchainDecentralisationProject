import pandas as pd
import json
import networkx as nx
from collections import defaultdict
from itertools import combinations
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import csv

# If the data is stored in a file:
file_path = "filtered_prs_BTC.json"

with open(file_path, "r") as f:
    prs = json.load(f)

# Create a dictionary to store graphs per month
monthly_graphs = defaultdict(nx.DiGraph)

# Iterate over each PR and populate the corresponding monthly graph
for pr in prs:
    author = pr["user"]
    commenters = pr["commenters"]
    reviewers = pr["reviewers"]
    
    # Parse timestamp, assuming "created_at" is present in each PR (e.g., ISO format)
    pr_date = datetime.fromisoformat(pr["created_at"])
    month_key = pr_date.strftime('%Y-%m')  # Format: "2025-04"

    # Ensure graph exists for this month
    G = monthly_graphs[month_key]

    G.add_node(author)

    for commenter in commenters:
        G.add_node(commenter)
        if commenter != author:
            G.add_edge(commenter, author, weight = 1)  # Add edge from author to commenter
    
    for reviewer in reviewers:
        G.add_node(reviewer)
        if reviewer != author:
            G.add_edge(reviewer, author, weight = 5)  # Add edge from author to reviewer

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

quarterly_graphs = defaultdict(nx.DiGraph)

for month, G in monthly_graphs.items():
    year, m = map(int, month.split('-'))
    quarter = (m - 1) // 3 + 1
    quarter_key = f'{year}-Q{quarter}'
    quarterly_graphs[quarter_key] = nx.compose(quarterly_graphs[quarter_key], G)

# Compute centralities per quarter
quarterly_centralities = {}
for quarter, G in quarterly_graphs.items():
    centrality = nx.degree_centrality(G)  # or nx.degree(G) if you want raw degree
    quarterly_centralities[quarter] = centrality

#Calc Degree
totalDeg = {}
for month, G in monthly_graphs.items():
    centrality = dict(G.degree(weight='weight'))
    monthly_centralities[month] = centrality
    totalDeg[month] = sum(centrality.values())

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

#Calc betweenness

for month, centrality_dict in monthly_centralities.items():
    centrality_values = list(centrality_dict.values())
    monthly_gini[month] = gini(centrality_values)
    #degSums = list(totalDeg)

result_df_btw = pd.DataFrame({
    'Quarter': list(quarterly_centralities.keys()),
    #'gini_coefficient': list(monthly_gini.values()),
})

result_df = pd.DataFrame({
    'Month': list(monthly_centralities.keys()),
    'Gini coefficient': list(monthly_gini.values()),
    'Degree Sum': list(totalDeg.values())
})


# Example betweenness centrality for top nodes each month:
result_df_btw['top_5_nodes'] = [
    sorted(c.items(), key=lambda x: x[1], reverse=True)[:5] for c in quarterly_centralities.values()
]

print(result_df_btw)

result_df_btw.to_csv("timeSeriesBetw_BTC2.csv", index=False)
result_df.to_csv("timeSeries_BTC.csv", index=False)

result_df.set_index('Month', inplace=True)

plt.figure(figsize=(12,6))
plt.plot(result_df.index, result_df['Gini coefficient'], marker='o', linestyle='-')
plt.title('Monthly Gini Coefficient for Degree Centrality')
plt.ylabel('Gini Coefficient')
plt.xlabel('Month')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()
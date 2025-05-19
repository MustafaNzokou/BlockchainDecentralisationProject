import matplotlib.pyplot as plt

# Full top 5 per network
users = [
    'lightclient', 'SamWilsn', 'MicahZoltu', 'axic', 'Pandapip1',        # ETC
    'luke-jr', 'sipa', 'jonatack', 'murchandamus', 'achow101',           # BTC
    'rphair', 'KtorZ', 'Ryun1', 'SebastienGllmt', 'michaelpj'            # ADA
]
degree_scores = [
    437, 411, 373, 332, 327,
    389, 167, 144, 130, 114,
    206, 172, 138, 113, 91
]
tokens = [
    'ETC', 'ETC', 'ETC', 'ETC', 'ETC',
    'BTC', 'BTC', 'BTC', 'BTC', 'BTC',
    'ADA', 'ADA', 'ADA', 'ADA', 'ADA'
]
# Assign colors per token
colors = ['green'] * 5 + ['gold'] * 5 + ['blue'] * 5

# Create figure
plt.figure(figsize=(14, 6))
bars = plt.bar(users, degree_scores, color=colors)

# Add value labels above bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 5, int(yval), ha='center', fontsize=8)

# Aesthetic settings
plt.title('Top 5 Contributors by Degree Centrality per Blockchain', fontsize=14)
plt.xlabel('User', fontsize=12)
plt.ylabel('Degree Score', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()

# Legend
plt.legend(handles=[
    plt.Rectangle((0,0),1,1,color='green', label='Ethereum Classic'),
    plt.Rectangle((0,0),1,1,color='gold', label='Bitcoin'),
    plt.Rectangle((0,0),1,1,color='blue', label='Cardano')
])

# Save and show
plt.savefig('top5_degree_centrality_all.png', dpi=300)
plt.show()

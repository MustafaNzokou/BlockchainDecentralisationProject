import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Read CSV
df = pd.read_csv('timeSeries_ADA.csv')

# Convert Month column to datetime
df['Month'] = pd.to_datetime(df['Month'])
df = df.sort_values('Month')

# Set up figure and axis
plt.style.use('ggplot')  # Cleaner look
fig, ax1 = plt.subplots(figsize=(10, 6))

# Plot Gini coefficient on left y-axis
color1 = 'tab:blue'
ax1.set_xlabel('Month', fontsize=12)
ax1.set_ylabel('Gini Coefficient', color=color1, fontsize=12)
ax1.plot(df['Month'], df['Gini coefficient'], color=color1, marker='o', linewidth=2, label='Gini Coefficient')
ax1.tick_params(axis='y', labelcolor=color1)
ax1.set_ylim(0, 1)

# Format x-axis as monthly ticks
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
fig.autofmt_xdate(rotation=45)

# Plot Degree Sum on right y-axis
ax2 = ax1.twinx()
color2 = 'tab:green'
ax2.set_ylabel('Degree Sum', color=color2, fontsize=12)
ax2.plot(df['Month'], df['Degree Sum'], color=color2, marker='s', linewidth=2, label='Degree Sum')
ax2.tick_params(axis='y', labelcolor=color2)

# Title and legend
plt.title('Evolution of Gini Coefficient and Degree Sum Over Time', fontsize=14, pad=15)
fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.9), frameon=False)

# Save figure
plt.tight_layout()
plt.savefig('gini_degree_timeseries.pdf', dpi=300)
plt.savefig('gini_degree_timeseries.png', dpi=300)
plt.show()

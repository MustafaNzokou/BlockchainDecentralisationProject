import pandas as pd

# Load JSON
df = pd.read_json("filtered_prs.json")

# Convert lists (reviewers/commenters) to strings for easier filtering
df["reviewers"] = df["reviewers"].apply(lambda x: ", ".join(x) if x else "No reviewers")
#df["commenters"] = df["commenters"].apply(lambda x: ", ".join(x) if x else "No commenters")

# Save to CSV (optional)
df.to_csv("filtered_prs.csv", index=False)

# Display first few rows
print(df.head())

# Example: Get PRs with the most reviewers
print(df.explode("reviewers").groupby("reviewers").size().sort_values(ascending=False))

import pandas as pd

df = pd.read_csv("2024_Parts_List.csv")

# Drop the "Full Plasmid Seq" column
df = df.drop(columns=["Full Plasmid Seq"])

# Save to json
df.to_json("results/index.json", orient="records", indent=2)

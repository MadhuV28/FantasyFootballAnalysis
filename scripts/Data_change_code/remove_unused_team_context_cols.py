import pandas as pd

csv_path = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/pos_combined_year/team_context_all_years.csv"
df = pd.read_csv(csv_path)

# Remove the specified columns if they exist
df = df.drop(columns=["RedZone_Plays", "Team_AirYards"], errors="ignore")

df.to_csv(csv_path, index=False)
print("Removed RedZone_Plays and Team_AirYards columns from the dataset.")
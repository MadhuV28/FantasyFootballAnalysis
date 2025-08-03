import pandas as pd

infile = "/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/pos_combined_year/team_context_all_years.csv"
outfile = infile  # Overwrite with cleaned version

df = pd.read_csv(infile)

# Remove rows with non-data headers or empty values
df = df[
    (~df['Team'].isna()) &
    (~df['Year'].isna()) &
    (df['Team'].str.strip().str.upper() != "TEAM ABBREVIATION") &
    (df['Year'].astype(str).str.lower() != "season year") &
    (df['Team'].str.strip() != "") &
    (df['Year'].astype(str).str.strip() != "")
]

# Optionally, reset index and sort
df = df.reset_index(drop=True)

df.to_csv(outfile, index=False)
print(f"Cleaned and saved: {outfile}")
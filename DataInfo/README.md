DataInfo Folder Overview
The DataInfo folder contains all the core data sources used for Fantasy Football analytics and modeling in this project. The structure is designed for clarity, scalability, and ease of use for both exploratory analysis and modeling.

Folder & File Structure

1. pos_combined_year/
    Purpose: Contains combined and modeling-ready datasets for all positions and years.

Key Files:
    modeling_final_enriched.csv
        All players, all stats, all years.
        This is the most comprehensive file, including every stat field for every player, regardless of whether all fields are populated.

    modeling_final.csv
        All players, generic/important stats only.
        A more concise version with only the most relevant features for modeling.

    fantasy_skill_positions.csv
        WR, RB, TE only, with general stats.
        Focuses on the main fantasy skill positions, combining their data for cross-positional analysis.

    wr_all_years.csv, rb_all_years.csv, te_all_years.csv, 
        qb_all_years.csv
        Position-specific, all-year datasets.
        Each file contains all years for a single position.
    
        wr_modeling.csv, rb_modeling.csv, te_modeling.csv, qb_modeling.csv
        Position-specific, all-year, modeling-ready datasets.
        These are typically feature-engineered and ready for input into machine learning models.

2. wr/, rb/, te/, qb/
    Purpose: Contains year-specific, position-specific merged data.
    Example:
        2015WR_merged.csv, 2016RB_merged.csv, etc.
    Usage:
        Useful for detailed, position-by-position, year-by-year analysis or for building custom aggregations.

3. team_context/
    Purpose: Contains team-level statistics for each year.
    Example:
        team_context_2015.csv, team_context_2016.csv, etc.
    Usage:
        Useful for adding team context (e.g., offensive line grades, team pace, etc.) to player-level datasets.

4. General Notes
    Raw vs. Processed:
        Most files here are processed/merged and ready for analysis or modeling. If you have raw downloads, consider a separate raw/ folder.
    Naming Conventions:
        *_merged.csv: Merged data for a specific position and year.
        *_modeling.csv: Feature-engineered, modeling-ready data.
        *_all_years.csv: All years for a given position.
        modeling_final*.csv: All positions, all years, for modeling.
    Missing Data:
        Some files (especially modeling_final_enriched.csv) may have missing values for certain stats, depending on player position and data availability.

How to Use

    Exploratory Analysis:
        Use the position/year-specific files for deep dives or trend analysis.
    Modeling:
        Use the modeling_final.csv or modeling_final_enriched.csv for training machine learning models.
    Cross-Position Analysis:
        Use fantasy_skill_positions.csv or the combined files in pos_combined_year/.
    Team Context:
        Join team-level files to player-level data for richer features.

Example Workflow
    Load player-level data from pos_combined_year/modeling_final_enriched.csv.
    Join team context from team_context/ based on year and team.
    Filter or aggregate as needed for your analysis or modeling task.
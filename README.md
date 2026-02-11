# Fantasy Analytics Project
  ##2017 RB DATA IN UNAVAILABLE. ISSUE WHEN CLEANING DATA*************

## Overview
The Fantasy Analytics Project is designed to analyze and visualize NFL statistics, providing insights for fantasy football enthusiasts. This project pulls real NFL data, processes it, and generates visualizations to aid in decision-making.

## Project Structure
```
FantasyAnalyticsProject/
├── .vscode/                # VS Code settings
├── venv/                   # Python virtual environment
├── data/                   # Raw + processed CSVs
├── scripts/                # Python + R scripts
│   ├── pull_data.R         # Pull real NFL stats
│   └── merge_clean.py      # Merge + clean datasets
├── visualizations/         # Exploratory charts
├── models/                 # Regression + ML outputs
├── requirements.txt        # Python dependencies
└── README.md               # Instructions
```

## Setup Instructions
1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd FantasyAnalyticsProject
   ```

2. **Create a Python virtual environment**:
   ```
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. **Install the required dependencies**:
   ```
   pip install -r requirements.txt
   ```

## Usage
- To pull NFL statistics, run the R script:
  ```
  Rscript scripts/pull_data.R
  ```

- To merge and clean datasets, execute the Python script:
  ```
  python scripts/merge_clean.py
  ```

- Visualizations can be found in the `visualizations/` directory.


Automated Data Update Pipeline (auto_update_data.py)
Built a Python script that automatically pulls the latest NFL player projections and metadata from the Sleeper API, merges and flattens the data into a clean, model-ready format, and saves it as an updated CSV for analytics and dashboards. This removes manual data refreshes, keeps projections current, and enables scheduled updates for a production-style fantasy football analytics pipeline.


## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any suggestions or improvements.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
<<<<<<< HEAD
=======



lets try: 
Deploy as a web app: Make your Streamlit dashboard public for others to use.
Enhance GUI usability: Add more visualizations (heatmaps, bar charts), export options, and user-friendly controls.
Improve model explainability: Use SHAP or feature importance plots to show why the model recommends certain players.
Add player injury history and news integration: Use APIs to pull recent injury reports or player news for context.

Here are several AI and ML enhancements you could add to your fantasy football analytics project:

**1. Advanced Player Projections**
- Use deep learning (e.g., LSTM, GRU) to forecast player performance based on historical stats, injuries, and team context.
- Ensemble multiple models (regression, tree-based, neural nets) for more robust projections.

**2. Draft Strategy Optimization**
- Reinforcement learning to simulate and optimize draft strategies for different league formats.
- Genetic algorithms to evolve draft strategies based on simulated league outcomes.

**3. Trade and Waiver Recommendation Engine**
- Build ML models to recommend trades and waiver pickups based on projected value, team needs, and league trends.

<!-- **4. Injury Risk Prediction**
- Train models to predict injury risk using player history, workload, and medical reports.

**5. Model Explainability**
- Integrate SHAP or LIME to explain why the model recommends certain players or strategies. -->

**6. Real-Time Data Integration**
- Use NLP to analyze player news, tweets, and injury reports for dynamic projection updates.

**7. Personalized Recommendations**
- Use collaborative filtering or user profiling to recommend draft picks and roster moves tailored to each user’s preferences and league history.

**8. Simulation-Based Season Outcomes**
- Monte Carlo simulations to estimate playoff odds, championship probability, and optimal weekly lineups.

**9. Automated Data Labeling**
- Use AI to extract and label player stats from web sources or PDFs.

**10. Visual Analytics**
- Build interactive dashboards with AI-driven insights (e.g., clustering, anomaly detection, trend forecasting).

---


(Model Context Protocol
>>>>>>> ba8adeb (push all changes before web app deployment)

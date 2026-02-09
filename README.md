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

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any suggestions or improvements.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

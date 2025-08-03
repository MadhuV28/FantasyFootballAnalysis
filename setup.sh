#!/bin/bash
echo "Setting up Fantasy Analytics Project..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install --upgrade pip
pip install pandas numpy matplotlib seaborn plotly scikit-learn xgboost jupyter

# Save requirements
pip freeze > requirements.txt

# Install R packages (run Rscript non-interactively)
Rscript -e 'install.packages(c("nflfastR","dplyr","tidyr","readr"), repos="http://cran.us.r-project.org")'

echo "Setup complete. Open VS Code and select this folder."

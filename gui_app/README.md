# gui_app Folder Overview

The `gui_app` folder contains all the code for the interactive graphical user interfaces (GUIs) used in this Fantasy Football analytics project. The structure separates frontend (user interface) code from backend (data processing and logic) code for clarity, maintainability, and scalability.

---

## Folder & File Structure

### 1. **backend/**
- **Purpose:** Contains all backend logic, including data loading, cleaning, filtering, and calculations.
- **Key Files:**
  - **app_backend.py**  
    Backend functions for the main analytics app (data manipulation, filtering, etc.).
  - **clusters_backend.py**  
    Backend functions specifically for clustering features (e.g., KMeans clustering logic).

---

### 2. **gui/**
- **Purpose:** Contains all frontend code for the GUIs, built with Tkinter.
- **Key Files:**
  - **app_gui.py**  
    Main GUI for data exploration, filtering, and visualization.
  - **clusters_gui.py**  
    GUI for clustering analysis and visualization.

---

## How It Works

- **Frontend (gui/):**  
  Handles all user interface elements, user interactions, and visualization display.  
  Calls backend functions to fetch, filter, and process data as needed.
- **Backend (backend/):**  
  Handles all data-related operations, including loading CSVs, filtering by user selections, and performing calculations or clustering.

---

## Usage

1. **Run a GUI:**  
   Navigate to the `gui_app/gui` directory and run the desired GUI script, for example:
   ```
   python app_gui.py
   ```
   or
   ```
   python clusters_gui.py
   ```
2. **Interacting:**  
   Use the GUI to select years, positions, players, and other filters. Visualizations and analyses update in real time based on your selections.

---

## Best Practices

- **Separation of Concerns:**  
  All data logic is in the backend; all UI logic is in the frontend. This makes the codebase easier to maintain and extend.
- **Naming Conventions:**  
  - Files ending with `_gui.py` are for the frontend.
  - Files ending with `_backend.py` are for backend logic.
- **Extensibility:**  
  New features or analyses can be added by creating new backend/frontend pairs.

---

## Example Workflow

1. **User launches the GUI** and selects filters (e.g., year, position, player).
2. **Frontend calls backend functions** to load and filter data.
3. **Backend returns processed data** to the frontend.
4. **Frontend displays updated visualizations** or analysis results.

---

## Contact

For questions about the GUI code or structure, please refer to the project documentation or contact the project maintainers.


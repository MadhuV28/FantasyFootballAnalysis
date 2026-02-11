import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import pandas.api.types as ptypes

st.set_page_config(layout="wide")
st.markdown("<h2 style='text-align: center; font-size: 1.2rem;'>Fantasy Analytics Dashboard</h2>", unsafe_allow_html=True)

# --- Load your position-specific feature correlations ---
# Example: Replace with your actual loading logic
correlations = {
    "QB": pd.read_csv("gui_app/gui/data/QB_feature_correlations.csv"),
    "RB": pd.read_csv("gui_app/gui/data/RB_feature_correlations.csv"),
    "WR": pd.read_csv("gui_app/gui/data/WR_feature_correlations.csv"),
    "TE": pd.read_csv("gui_app/gui/data/TE_feature_correlations.csv"),
}

st.markdown("## Feature Correlations by Position")

cols = st.columns(4)
positions = ["QB", "RB", "WR", "TE"]
for i, pos in enumerate(positions):
    with cols[i]:
        st.markdown(f"**{pos} Feature Correlations**")
        # Scrollable section using st.dataframe with height limit
        st.dataframe(correlations[pos], height=150)  # Adjust height as needed
# ----------- TOP QUADRANTS: SHARED FILTERS & PLOTS -----------
top_left_col, top_right_col = st.columns(2)

# --- FILTERS SECTION ---
with st.container():
    df_top = pd.read_csv('/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/pos_combined_year/modeling_final_enriched.csv')
    for col in df_top.columns:
        if '%' in col:
            df_top[col] = (
                df_top[col]
                .astype(str)
                .str.rstrip('%')
                .replace('', 'NaN')
                .astype(float)
                .round()
                .astype('Int64')
            )
    df_top['Rank'] = df_top.groupby(['Year', 'Position'])['Fantasy Points'].rank(method='first', ascending=False)
    def rank_group(r):
        if r <= 5:
            return 'Top 5'
        elif r <= 10:
            return '6-10'
        elif r <= 20:
            return '11-20'
        else:
            return '21+'
    df_top['Group'] = df_top['Rank'].apply(rank_group)

    columns = list(df_top.columns)
    positions = sorted(df_top['Position'].dropna().unique())
    years = sorted(df_top['Year'].dropna().astype(str).unique())

    st.markdown("<div style='font-size:0.8rem;'>Shared Filters (App GUI & Clusters GUI)</div>", unsafe_allow_html=True)
    selected_years = st.multiselect("Year(s):", years, default=years, key="shared_years")
    selected_positions = st.multiselect("Position(s):", positions, default=positions, key="shared_positions")
    x_axis = st.selectbox("X Axis:", columns, index=0, key="shared_x")
    y_axis = st.selectbox("Y Axis:", columns, index=1, key="shared_y")

    filtered_top = df_top.copy()
    if selected_positions:
        filtered_top = filtered_top[filtered_top['Position'].isin(selected_positions)]
    if selected_years:
        filtered_top = filtered_top[filtered_top['Year'].astype(str).isin(selected_years)]

    player_options = sorted(filtered_top['Player'].dropna().unique())
    player_search = st.text_input("Search Player:", key="shared_player_search")
    if player_search:
        player_options = [p for p in player_options if player_search.lower() in p.lower()]
    selected_players = st.multiselect("Player(s):", player_options, key="shared_players")

    highlight_options = player_options if selected_players else sorted(filtered_top['Player'].dropna().unique())
    highlight_search = st.text_input("Search Highlight Player:", key="shared_highlight_search")
    if highlight_search:
        highlight_options = [p for p in highlight_options if highlight_search.lower() in p.lower()]
    highlight_players = st.multiselect("Highlight Player(s):", highlight_options, key="shared_highlights")

    n_clusters = st.slider("Number of Clusters (Clusters GUI only):", min_value=2, max_value=10, value=3, key="shared_clusternum")

# --- PLOTS SECTION (below filters) ---
if "show_top_plots" not in st.session_state:
    st.session_state["show_top_plots"] = False

if st.button("Plot Top Quadrants", key="shared_plot"):
    st.session_state["show_top_plots"] = True

if st.session_state["show_top_plots"]:
    plot_cols = st.columns(2)
    with plot_cols[0]:
        with st.container():
            st.markdown("<h4 style='font-size:0.9rem;'>App GUI (Top Left)</h4>", unsafe_allow_html=True)
            plot_df = filtered_top.copy()
            if selected_players:
                plot_df = plot_df[plot_df['Player'].isin(selected_players)]
            if plot_df.empty:
                st.warning("No data for selection (0 records matched)")
            else:
                is_numeric_x = ptypes.is_numeric_dtype(plot_df[x_axis])
                is_numeric_y = ptypes.is_numeric_dtype(plot_df[y_axis])

                if is_numeric_x and is_numeric_y:
                    # Calculate correlation
                    try:
                        corr = plot_df[x_axis].corr(plot_df[y_axis])
                    except Exception:
                        corr = None
                    st.markdown(f"**Feature Correlation ({x_axis} vs {y_axis}):** {corr:.3f}" if corr is not None else "**Feature Correlation:** N/A")

                    # Plotly scatter with trendline
                    fig = px.scatter(
                        plot_df,
                        x=x_axis,
                        y=y_axis,
                        color="Group",
                        color_discrete_map={'Top 5': 'red', '6-10': 'orange', '11-20': 'green', '21+': 'blue'},
                        hover_data=["Player", "Year", "Position", x_axis, y_axis],
                        trendline="ols"
                    )
                else:
                    st.markdown("**Feature Correlation:** N/A (select numeric columns for both axes)")
                    fig = px.scatter(
                        plot_df,
                        x=x_axis,
                        y=y_axis,
                        color="Group",
                        color_discrete_map={'Top 5': 'red', '6-10': 'orange', '11-20': 'green', '21+': 'blue'},
                        hover_data=["Player", "Year", "Position", x_axis, y_axis]
                        # Do NOT add trendline
                    )
                fig.update_layout(
                    title=f"{y_axis} vs {x_axis}",
                    legend_title="Group",
                    height=300,
                    margin=dict(l=0, r=0, t=30, b=0)
                )
                st.plotly_chart(fig, use_container_width=True)

    with plot_cols[1]:
        with st.container():
            st.markdown("<h4 style='font-size:0.9rem;'>Clusters GUI (Top Right)</h4>", unsafe_allow_html=True)
            plot_df = filtered_top.copy()
            if selected_players:
                plot_df = plot_df[plot_df['Player'].isin(selected_players)]
            plot_df[x_axis] = plot_df[x_axis].astype(str).str.replace(',', '', regex=False)
            plot_df[y_axis] = plot_df[y_axis].astype(str).str.replace(',', '', regex=False)
            plot_df = plot_df.dropna(subset=[x_axis, y_axis])
            try:
                plot_df[x_axis] = pd.to_numeric(plot_df[x_axis], errors='raise')
                plot_df[y_axis] = pd.to_numeric(plot_df[y_axis], errors='raise')
            except Exception:
                st.error(f"Selected axis columns must be numeric.\nYou chose:\nX: {x_axis}\nY: {y_axis}")
            else:
                # Calculate correlation
                try:
                    corr = plot_df[x_axis].corr(plot_df[y_axis])
                except Exception:
                    corr = None
                st.markdown(f"**Feature Correlation ({x_axis} vs {y_axis}):** {corr:.3f}" if corr is not None else "**Feature Correlation:** N/A")

                from sklearn.cluster import KMeans
                from sklearn.preprocessing import StandardScaler
                X = plot_df[[x_axis, y_axis]].astype(float).to_numpy()
                scaler = StandardScaler()
                X_scaled = scaler.fit_transform(X)
                kmeans = KMeans(n_clusters=n_clusters, n_init=10, random_state=42)
                clusters = kmeans.fit_predict(X_scaled)
                plot_df['Cluster'] = clusters
                fig = px.scatter(
                    plot_df,
                    x=x_axis,
                    y=y_axis,
                    color="Cluster",
                    hover_data=["Player", "Year", "Position", x_axis, y_axis],
                    trendline="ols"
                )
                fig.update_layout(
                    title=f"KMeans Clustering: {y_axis} vs {x_axis}",
                    legend_title="Cluster",
                    height=300,
                    margin=dict(l=0, r=0, t=30, b=0)
                )
                st.plotly_chart(fig, use_container_width=True)

# ----------- BOTTOM QUADRANTS: SHARED FILTERS & PLOTS -----------
st.markdown("---")
bottom_left_col, bottom_right_col = st.columns(2)

# Filter section
with st.container():
    df_adp = pd.read_csv('/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/2025_ADP_VORP.csv')
    df_adp = df_adp[['Rank', 'Player', 'Team', 'POS', 'AVG', 'VORP', 'VORPvsADP']].copy()
    def group_pos(pos):
        pos = str(pos).upper()
        for prefix in ['QB', 'RB', 'WR', 'TE', 'DST', 'K']:
            if pos.startswith(prefix): return prefix
        return pos
    df_adp['POS_GROUP'] = df_adp['POS'].apply(group_pos)
    for col in ['AVG', 'VORP']:
        df_adp[col] = pd.to_numeric(df_adp[col], errors='coerce')
    def clean_vorp_vs_adp(val):
        if pd.isnull(val): return np.nan
        val = str(val).replace('+', '').replace(' ', '')
        try: return float(val)
        except: return np.nan
    df_adp['VORPvsADP_clean'] = df_adp['VORPvsADP'].apply(clean_vorp_vs_adp)

    positions = ['QB', 'RB', 'WR', 'TE', 'DST', 'K']
    axis_options = ['AVG', 'VORP', 'VORPvsADP_clean']
    axis_labels = {'AVG': 'ADP AVG', 'VORP': 'VORP', 'VORPvsADP_clean': 'VORP vs ADP'}

    st.markdown("<div style='font-size:0.8rem;'>Shared Filters (ADP VORP GUI & ADP VORP KMeans GUI)</div>", unsafe_allow_html=True)
    selected_positions = st.multiselect("Position(s):", positions, default=positions, key="adp_shared_positions")
    x_axis_label = st.selectbox("X Axis:", [axis_labels[a] for a in axis_options], index=0, key="adp_shared_x")
    y_axis_label = st.selectbox("Y Axis:", [axis_labels[a] for a in axis_options], index=1, key="adp_shared_y")
    axis_map = {v: k for k, v in axis_labels.items()}
    x_axis = axis_map[x_axis_label]
    y_axis = axis_map[y_axis_label]

    filtered_adp = df_adp[df_adp['POS_GROUP'].isin(selected_positions)]
    player_options = sorted(filtered_adp['Player'].dropna().unique())
    player_search = st.text_input("Search Player:", key="adp_shared_player_search")
    if player_search:
        player_options = [p for p in player_options if player_search.lower() in p.lower()]
    selected_players = st.multiselect("Player(s):", player_options, key="adp_shared_players")

    highlight_options = player_options if selected_players else sorted(filtered_adp['Player'].dropna().unique())
    highlight_search = st.text_input("Search Highlight Player:", key="adp_shared_highlight_search")
    if highlight_search:
        highlight_options = [p for p in highlight_options if highlight_search.lower() in p.lower()]
    highlight_players = st.multiselect("Highlight Player(s):", highlight_options, key="adp_shared_highlights")

    n_clusters = st.slider("Number of Clusters (ADP VORP KMeans only):", min_value=2, max_value=10, value=3, key="adp_shared_clusternum")

# Plot section (below filters)
if "show_bottom_plots" not in st.session_state:
    st.session_state["show_bottom_plots"] = False

if st.button("Plot Bottom Quadrants", key="adp_shared_plot"):
    st.session_state["show_bottom_plots"] = True

if st.session_state["show_bottom_plots"]:
    with bottom_left_col:
        with st.container():
            st.markdown("<h4 style='font-size:0.9rem;'>ADP VORP GUI (Bottom Left)</h4>", unsafe_allow_html=True)
            plot_df = filtered_adp[(filtered_adp['AVG'] <= 300)].copy()
            if selected_players:
                plot_df = plot_df[plot_df['Player'].isin(selected_players)]
            plot_df = plot_df.dropna(subset=[x_axis, y_axis])
            if plot_df.empty:
                st.warning("No data for selection (0 records matched)")
            else:
                fig = px.scatter(
                    plot_df,
                    x=x_axis,
                    y=y_axis,
                    color="POS_GROUP",
                    color_discrete_map={'RB': 'green', 'WR': 'blue', 'TE': 'orange', 'QB': 'red', 'K': 'purple', 'DST': 'gray'},
                    hover_data=["Player", "Team", "POS", x_axis, y_axis]
                )
                fig.update_layout(
                    title=f"ADP VORP: {y_axis_label} vs {x_axis_label}",
                    legend_title="Position",
                    height=300,
                    margin=dict(l=0, r=0, t=30, b=0)
                )
                st.plotly_chart(fig, use_container_width=True)

    with bottom_right_col:
        with st.container():
            st.markdown("<h4 style='font-size:0.9rem;'>ADP VORP KMeans GUI (Bottom Right)</h4>", unsafe_allow_html=True)
            plot_df = filtered_adp[(filtered_adp['AVG'] <= 300)].copy()
            if selected_players:
                plot_df = plot_df[plot_df['Player'].isin(selected_players)]
            plot_df = plot_df.dropna(subset=[x_axis, y_axis])
            try:
                plot_df[x_axis] = pd.to_numeric(plot_df[x_axis], errors='raise')
                plot_df[y_axis] = pd.to_numeric(plot_df[y_axis], errors='raise')
            except Exception:
                st.error(f"Selected axis columns must be numeric.\nYou chose:\nX: {x_axis}\nY: {y_axis}")
            else:
                from sklearn.cluster import KMeans
                from sklearn.preprocessing import StandardScaler
                X = plot_df[[x_axis, y_axis]].astype(float).to_numpy()
                scaler = StandardScaler()
                X_scaled = scaler.fit_transform(X)
                kmeans = KMeans(n_clusters=n_clusters, n_init=10, random_state=42)
                clusters = kmeans.fit_predict(X_scaled)
                plot_df['Cluster'] = clusters
                fig = px.scatter(
                    plot_df,
                    x=x_axis,
                    y=y_axis,
                    color="Cluster",
                    hover_data=["Player", "Team", "POS", x_axis, y_axis]
                )
                fig.update_layout(
                    title=f"ADP VORP KMeans: {y_axis_label} vs {x_axis_label}",
                    legend_title="Cluster",
                    height=300,
                    margin=dict(l=0, r=0, t=30, b=0)
                )
                st.plotly_chart(fig, use_container_width=True)
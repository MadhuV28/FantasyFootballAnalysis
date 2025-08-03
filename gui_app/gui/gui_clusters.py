# from backend.backend_gui_clusters import (
#     load_data, filter_df, get_unique_sorted, run_kmeans
# )

# df = load_data('/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/pos_combined_year/modeling_final_enriched.csv')

# positions = get_unique_sorted(df, 'Position')
# years = get_unique_sorted(df, 'Year')

# from backend.backend_gui_clusters import (
#     load_data, filter_df, get_unique_sorted, run_kmeans
# )

# import tkinter as tk
# from tkinter import ttk, messagebox
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import matplotlib.pyplot as plt
# import mplcursors

# df = load_data('/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/pos_combined_year/modeling_final_enriched.csv')
# positions = get_unique_sorted(df, 'Position')
# years = get_unique_sorted(df, 'Year')
# columns = list(df.columns)

# active_cursors = []
# plot_canvas = None
# highlighted_players_set = set()
# selected_players_set = set()

# window = tk.Tk()
# window.title("Fantasy Analytics KMeans Clustering")
# window.geometry("1000x750")

# window.rowconfigure(0, weight=1)
# window.columnconfigure(0, weight=1)

# canvas = tk.Canvas(window)
# scrollbar = ttk.Scrollbar(window, orient="vertical", command=canvas.yview)
# canvas.configure(yscrollcommand=scrollbar.set)
# canvas.grid(row=0, column=0, sticky="nsew")
# scrollbar.grid(row=0, column=1, sticky="ns")

# content_frame = ttk.Frame(canvas)
# content_frame_id = canvas.create_window((0, 0), window=content_frame, anchor="nw")

# def on_configure(event):
#     canvas.configure(scrollregion=canvas.bbox("all"))
#     canvas.itemconfig(content_frame_id, width=canvas.winfo_width())
# content_frame.bind("<Configure>", on_configure)
# canvas.bind("<Configure>", on_configure)

# for i in range(4):
#     content_frame.columnconfigure(i, weight=1)
# for i in range(9):
#     content_frame.rowconfigure(i, weight=1)

# # --- Years and Positions side by side ---
# ttk.Label(content_frame, text="Year(s):").grid(row=0, column=0, sticky='ew')
# year_frame = ttk.Frame(content_frame)
# year_frame.grid(row=0, column=1, sticky='nsew', pady=2)
# year_listbox = tk.Listbox(year_frame, selectmode='multiple', exportselection=0, height=3)
# year_scroll = ttk.Scrollbar(year_frame, orient="vertical", command=year_listbox.yview)
# year_listbox.configure(yscrollcommand=year_scroll.set)
# year_listbox.pack(side="left", fill="both", expand=True)
# year_scroll.pack(side="right", fill="y")
# for y in years:
#     year_listbox.insert(tk.END, y)

# ttk.Label(content_frame, text="Position(s):").grid(row=0, column=2, sticky='ew')
# pos_frame = ttk.Frame(content_frame)
# pos_frame.grid(row=0, column=3, sticky='nsew', pady=2)
# pos_listbox = tk.Listbox(pos_frame, selectmode='multiple', exportselection=0, height=3)
# pos_scroll = ttk.Scrollbar(pos_frame, orient="vertical", command=pos_listbox.yview)
# pos_listbox.configure(yscrollcommand=pos_scroll.set)
# pos_listbox.pack(side="left", fill="both", expand=True)
# pos_scroll.pack(side="right", fill="y")
# for p in positions:
#     pos_listbox.insert(tk.END, p)

# x_var = tk.StringVar(value=columns[0])
# ttk.Label(content_frame, text="X Axis:").grid(row=2, column=0, sticky='ew')
# x_entry = ttk.Entry(content_frame, textvariable=x_var)
# x_entry.grid(row=2, column=1, sticky='nsew')
# x_dropdown = ttk.Combobox(content_frame, textvariable=x_var, values=columns)
# x_dropdown.grid(row=2, column=2, sticky='nsew')

# y_var = tk.StringVar(value=columns[1])
# ttk.Label(content_frame, text="Y Axis:").grid(row=3, column=0, sticky='ew')
# y_entry = ttk.Entry(content_frame, textvariable=y_var)
# y_entry.grid(row=3, column=1, sticky='nsew')
# y_dropdown = ttk.Combobox(content_frame, textvariable=y_var, values=columns)
# y_dropdown.grid(row=3, column=2, sticky='nsew')

# # --- Number of Clusters ---
# ttk.Label(content_frame, text="Clusters:").grid(row=4, column=0, sticky='ew')
# cluster_var = tk.IntVar(value=3)
# cluster_spin = ttk.Spinbox(content_frame, from_=2, to=10, textvariable=cluster_var, width=5)
# cluster_spin.grid(row=4, column=1, sticky='nsew')

# # --- Player and Highlight Player UI ---
# player_search_var = tk.StringVar()
# ttk.Label(content_frame, text="Search Player:").grid(row=4, column=2, sticky='ew')
# player_search_entry = ttk.Entry(content_frame, textvariable=player_search_var)
# player_search_entry.grid(row=4, column=3, sticky='nsew')

# ttk.Label(content_frame, text="Player(s):").grid(row=5, column=0, sticky='ew')
# player_listbox = tk.Listbox(content_frame, selectmode='multiple', exportselection=0, height=5)
# player_listbox.grid(row=5, column=1, sticky='nsew', pady=2)

# highlight_search_var = tk.StringVar()
# ttk.Label(content_frame, text="Search Highlight:").grid(row=5, column=2, sticky='ew')
# highlight_search_entry = ttk.Entry(content_frame, textvariable=highlight_search_var)
# highlight_search_entry.grid(row=5, column=3, sticky='nsew')

# ttk.Label(content_frame, text="Highlight Player(s):").grid(row=6, column=0, sticky='ew')
# highlight_player_listbox = tk.Listbox(content_frame, selectmode='multiple', exportselection=0, height=5)
# highlight_player_listbox.grid(row=6, column=1, sticky='nsew', pady=2)

# ttk.Button(content_frame, text="Cluster", command=lambda: plot_clusters()).grid(row=7, column=0, columnspan=4, sticky='nsew')

# selected_info_var = tk.StringVar()
# selected_info_label = ttk.Label(content_frame, textvariable=selected_info_var, anchor='w', justify='left', font=("Arial", 10))
# selected_info_label.grid(row=8, column=0, columnspan=4, sticky='nsew', padx=5, pady=5)

# def get_selected_years():
#     selected = [years[i] for i in year_listbox.curselection()]
#     return selected if selected else years

# def get_selected_positions():
#     selected = [positions[i] for i in pos_listbox.curselection()]
#     return selected if selected else positions

# def get_selected_players():
#     return list(selected_players_set)

# def get_highlight_players():
#     return list(highlighted_players_set)

# def update_axis_options(event, axis_var, entry, dropdown, columns):
#     typed = entry.get().lower()
#     matches = [col for col in columns if typed in col.lower()]
#     dropdown['values'] = matches if matches else columns
#     if event.keysym == "Return" and matches:
#         axis_var.set(matches[0])

# x_entry.bind('<KeyRelease>', lambda e: update_axis_options(e, x_var, x_entry, x_dropdown, columns))
# y_entry.bind('<KeyRelease>', lambda e: update_axis_options(e, y_var, y_entry, y_dropdown, columns))

# def update_player_listbox(*args):
#     pos_selected = get_selected_positions()
#     year_selected = get_selected_years()
#     search = player_search_var.get().lower()
#     filtered = filter_df(df, years=year_selected, positions=pos_selected)
#     player_options = sorted(filtered['Player'].dropna().unique())
#     if search:
#         player_options = [p for p in player_options if search in p.lower()]
#     player_listbox.delete(0, tk.END)
#     for p in player_options:
#         player_listbox.insert(tk.END, p)
#     for idx, p in enumerate(player_options):
#         if p in selected_players_set:
#             player_listbox.selection_set(idx)

# def player_search_event(event):
#     update_player_listbox()
#     if event.keysym == "Return":
#         search = player_search_var.get().lower()
#         for idx in range(player_listbox.size()):
#             player = player_listbox.get(idx)
#             if player.lower().startswith(search):
#                 player_listbox.selection_set(idx)
#                 selected_players_set.add(player)
#                 player_listbox.see(idx)
#                 break

# def on_player_listbox_select(event):
#     visible_players = [player_listbox.get(i) for i in range(player_listbox.size())]
#     selected_indices = player_listbox.curselection()
#     selected_players = set([player_listbox.get(i) for i in selected_indices])
#     for p in visible_players:
#         if p in selected_players_set and p not in selected_players:
#             selected_players_set.remove(p)
#     for p in selected_players:
#         selected_players_set.add(p)
#     update_highlight_player_listbox()

# def update_highlight_player_listbox(*args):
#     pos_selected = get_selected_positions()
#     year_selected = get_selected_years()
#     search = highlight_search_var.get().lower()
#     filtered = filter_df(df, years=year_selected, positions=pos_selected)
#     # If any players are selected, only show those. Otherwise, show all possible players.
#     if selected_players_set:
#         player_options = sorted(selected_players_set)
#     else:
#         player_options = sorted(filtered['Player'].dropna().unique())
#     if search:
#         player_options = [p for p in player_options if search in p.lower()]
#     highlight_player_listbox.delete(0, tk.END)
#     for p in player_options:
#         highlight_player_listbox.insert(tk.END, p)
#     for idx, p in enumerate(player_options):
#         if p in highlighted_players_set:
#             highlight_player_listbox.selection_set(idx)

# def highlight_search_event(event):
#     update_highlight_player_listbox()
#     if event.keysym == "Return":
#         search = highlight_search_var.get().lower()
#         for idx in range(highlight_player_listbox.size()):
#             player = highlight_player_listbox.get(idx)
#             if player.lower().startswith(search):
#                 highlight_player_listbox.selection_set(idx)
#                 highlighted_players_set.add(player)
#                 highlight_player_listbox.see(idx)
#                 break

# def on_highlight_listbox_select(event):
#     visible_players = [highlight_player_listbox.get(i) for i in range(highlight_player_listbox.size())]
#     selected_indices = highlight_player_listbox.curselection()
#     selected_players = set([highlight_player_listbox.get(i) for i in selected_indices])
#     for p in visible_players:
#         if p in highlighted_players_set and p not in selected_players:
#             highlighted_players_set.remove(p)
#     for p in selected_players:
#         highlighted_players_set.add(p)

# def sync_global_sets_with_visible_players():
#     visible_players = set([player_listbox.get(i) for i in range(player_listbox.size())])
#     to_remove = set()
#     for p in selected_players_set:
#         if p not in visible_players:
#             to_remove.add(p)
#     selected_players_set.difference_update(to_remove)
#     visible_highlight_players = set([highlight_player_listbox.get(i) for i in range(highlight_player_listbox.size())])
#     to_remove_highlight = set()
#     for p in highlighted_players_set:
#         if p not in visible_highlight_players:
#             to_remove_highlight.add(p)
#     highlighted_players_set.difference_update(to_remove_highlight)

# def on_year_or_pos_change(event=None):
#     update_player_listbox()
#     update_highlight_player_listbox()
#     sync_global_sets_with_visible_players()
#     plot_clusters()

# def plot_clusters():
#     global active_cursors, plot_canvas
#     try:
#         x = x_var.get()
#         y = y_var.get()
#         n_clusters = cluster_var.get()
#         pos_selected = get_selected_positions()
#         year_selected = get_selected_years()
#         selected_players = get_selected_players()
#         highlight_players = get_highlight_players()

#         filtered = filter_df(df, years=year_selected, positions=pos_selected, players=selected_players)
#         if filtered.empty:
#             fig, ax = plt.subplots()
#             ax.text(0.5, 0.5, f'No data for selection\n(0 records matched)', ha='center', va='center')
#             ax.set_axis_off()
#         else:
#             try:
#                 clustered, centers = run_kmeans(filtered, x, y, n_clusters)
#             except Exception:
#                 messagebox.showerror(
#                     "Invalid Axis Selection",
#                     f"Selected axis columns must be numeric.\nYou chose:\nX: {x}\nY: {y}"
#                 )
#                 return

#             colors = plt.cm.get_cmap('tab10', n_clusters)
#             fig, ax = plt.subplots()
#             for i in range(n_clusters):
#                 group = clustered[clustered['Cluster'] == i]
#                 ax.scatter(
#                     group[x],
#                     group[y],
#                     label=f'Cluster {i+1}',
#                     color=colors(i),
#                     alpha=0.6,
#                     s=30
#                 )
#             if highlight_players:
#                 highlight_df = clustered[clustered['Player'].isin(highlight_players)]
#                 if not highlight_df.empty:
#                     ax.scatter(
#                         highlight_df[x],
#                         highlight_df[y],
#                         s=120,
#                         facecolors='none',
#                         edgecolors='black',
#                         linewidths=2,
#                         label='Highlighted Player(s)',
#                         zorder=10
#                     )
#             ax.scatter(centers[:, 0], centers[:, 1], c='black', marker='x', s=60, linewidths=2, label='Centers')
#             ax.set_xlabel(x)
#             ax.set_ylabel(y)
#             ax.set_title(f'KMeans Clustering: {y} vs {x}')
#             ax.legend()
#             fig.tight_layout()

#             active_cursors = []
#             sc = ax.scatter(clustered[x], clustered[y], c=clustered['Cluster'], cmap='tab10', alpha=0)
#             cursor = mplcursors.cursor(sc, hover=False)
#             active_cursors.append(cursor)
#             @cursor.connect("add")
#             def on_add(sel):
#                 idx = sel.index
#                 player = clustered.iloc[idx]['Player']
#                 year_val = clustered.iloc[idx]['Year']
#                 cluster = clustered.iloc[idx]['Cluster']
#                 x_val = clustered.iloc[idx][x]
#                 y_val = clustered.iloc[idx][y]
#                 rank = clustered.iloc[idx]['Rank'] if 'Rank' in clustered.columns else 'N/A'
#                 text = (
#                     f"{player} ({year_val})\n"
#                     f"Cluster: {cluster+1}\n"
#                     f"Fantasy Rank: {int(rank) if rank != 'N/A' and not pd.isnull(rank) else 'N/A'}\n"
#                     f"{x}: {x_val}\n"
#                     f"{y}: {y_val}"
#                 )
#                 sel.annotation.set(text=text)
#                 selected_info_var.set(text)

#         if plot_canvas is not None:
#             plot_canvas.get_tk_widget().destroy()
#         plot_canvas_new = FigureCanvasTkAgg(fig, master=content_frame)
#         plot_canvas_new.get_tk_widget().grid(row=9, column=0, columnspan=4, sticky='nsew')
#         plot_canvas_new.draw()
#         plot_canvas = plot_canvas_new
#     except Exception as e:
#         import traceback
#         print("Exception in plot_clusters():", e)
#         traceback.print_exc()

# # Make only the plot row expandable
# for i in range(9):
#     content_frame.rowconfigure(i, weight=0)
# content_frame.rowconfigure(9, weight=1)
# for i in range(4):
#     content_frame.columnconfigure(i, weight=1)

# plot_clusters()

# year_listbox.bind('<<ListboxSelect>>', on_year_or_pos_change)
# pos_listbox.bind('<<ListboxSelect>>', on_year_or_pos_change)
# player_search_entry.bind('<KeyRelease>', player_search_event)
# player_listbox.bind('<<ListboxSelect>>', on_player_listbox_select)
# highlight_search_entry.bind('<KeyRelease>', highlight_search_event)
# highlight_player_listbox.bind('<<ListboxSelect>>', on_highlight_listbox_select)

# update_player_listbox()
# update_highlight_player_listbox()

# window.mainloop()













import pandas as pd
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import mplcursors
import os
import matplotlib
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np

matplotlib.use('TkAgg')

df = pd.read_csv('/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/pos_combined_year/modeling_final_enriched.csv')

# Clean and convert all percentage columns to integer (rounded)
for col in df.columns:
    if '%' in col:
        df[col] = (
            df[col]
            .astype(str)
            .str.rstrip('%')
            .replace('', 'NaN')
            .astype(float)
            .round()
            .astype('Int64')
        )

df['Rank'] = df.groupby(['Year', 'Position'])['Fantasy Points'].rank(method='first', ascending=False)
def rank_group(r):
    if r <= 5:
        return 'Top 5'
    elif r <= 10:
        return '6-10'
    elif r <= 20:
        return '11-20'
    else:
        return '21+'
df['Group'] = df['Rank'].apply(rank_group)

active_cursors = []
plot_canvas = None

# --- Global sets to persistently track highlighted and selected players ---
highlighted_players_set = set()
selected_players_set = set()

window = tk.Tk()
window.title("Fantasy Analytics KMeans Clustering")
window.geometry("900x700")

window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)

canvas = tk.Canvas(window)
scrollbar = ttk.Scrollbar(window, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)
canvas.grid(row=0, column=0, sticky="nsew")
scrollbar.grid(row=0, column=1, sticky="ns")

content_frame = ttk.Frame(canvas)
content_frame_id = canvas.create_window((0, 0), window=content_frame, anchor="nw")

def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas.itemconfig(content_frame_id, width=canvas.winfo_width())
content_frame.bind("<Configure>", on_configure)
canvas.bind("<Configure>", on_configure)

for i in range(4):
    content_frame.columnconfigure(i, weight=1)
for i in range(9):
    content_frame.rowconfigure(i, weight=1)

columns = list(df.columns)
positions = sorted(df['Position'].dropna().unique())
years = sorted(df['Year'].dropna().astype(str).unique())

# --- Years and Positions side by side ---
ttk.Label(content_frame, text="Year(s):").grid(row=0, column=0, sticky='ew')
year_frame = ttk.Frame(content_frame)
year_frame.grid(row=0, column=1, sticky='nsew', pady=2)
year_listbox = tk.Listbox(year_frame, selectmode='multiple', exportselection=0, height=3)
year_scroll = ttk.Scrollbar(year_frame, orient="vertical", command=year_listbox.yview)
year_listbox.configure(yscrollcommand=year_scroll.set)
year_listbox.pack(side="left", fill="both", expand=True)
year_scroll.pack(side="right", fill="y")
for y in years:
    year_listbox.insert(tk.END, y)

ttk.Label(content_frame, text="Position(s):").grid(row=0, column=2, sticky='ew')
pos_frame = ttk.Frame(content_frame)
pos_frame.grid(row=0, column=3, sticky='nsew', pady=2)
pos_listbox = tk.Listbox(pos_frame, selectmode='multiple', exportselection=0, height=3)
pos_scroll = ttk.Scrollbar(pos_frame, orient="vertical", command=pos_listbox.yview)
pos_listbox.configure(yscrollcommand=pos_scroll.set)
pos_listbox.pack(side="left", fill="both", expand=True)
pos_scroll.pack(side="right", fill="y")
for p in positions:
    pos_listbox.insert(tk.END, p)

x_var = tk.StringVar(value=columns[0])
ttk.Label(content_frame, text="X Axis:").grid(row=2, column=0, sticky='ew')
x_entry = ttk.Entry(content_frame, textvariable=x_var)
x_entry.grid(row=2, column=1, sticky='nsew')
x_dropdown = ttk.Combobox(content_frame, textvariable=x_var, values=columns)
x_dropdown.grid(row=2, column=2, sticky='nsew')

y_var = tk.StringVar(value=columns[1])
ttk.Label(content_frame, text="Y Axis:").grid(row=3, column=0, sticky='ew')
y_entry = ttk.Entry(content_frame, textvariable=y_var)
y_entry.grid(row=3, column=1, sticky='nsew')
y_dropdown = ttk.Combobox(content_frame, textvariable=y_var, values=columns)
y_dropdown.grid(row=3, column=2, sticky='nsew')

def update_axis_options(event, axis_var, entry, dropdown, columns):
    typed = entry.get().lower()
    matches = [col for col in columns if typed in col.lower()]
    dropdown['values'] = matches if matches else columns
    if event.keysym == "Return" and matches:
        axis_var.set(matches[0])

x_entry.bind('<KeyRelease>', lambda e: update_axis_options(e, x_var, x_entry, x_dropdown, columns))
y_entry.bind('<KeyRelease>', lambda e: update_axis_options(e, y_var, y_entry, y_dropdown, columns))

# --- Number of Clusters ---
ttk.Label(content_frame, text="Clusters:").grid(row=4, column=0, sticky='ew')
cluster_var = tk.IntVar(value=3)
cluster_spin = ttk.Spinbox(content_frame, from_=2, to=10, textvariable=cluster_var, width=5)
cluster_spin.grid(row=4, column=1, sticky='nsew')

# --- Search Entry for Player(s) ---
player_search_var = tk.StringVar()
ttk.Label(content_frame, text="Search Player:").grid(row=4, column=0, sticky='ew')
player_search_entry = ttk.Entry(content_frame, textvariable=player_search_var)
player_search_entry.grid(row=4, column=1, sticky='nsew')

# --- Multi-select Listbox for Player(s) ---
ttk.Label(content_frame, text="Player(s):").grid(row=5, column=0, sticky='ew')
player_listbox = tk.Listbox(content_frame, selectmode='multiple', exportselection=0, height=5)
player_listbox.grid(row=5, column=1, sticky='nsew', pady=2)

# --- Search Entry for Highlight Player(s) ---
highlight_search_var = tk.StringVar()
ttk.Label(content_frame, text="Search Highlight:").grid(row=4, column=2, sticky='ew')
highlight_search_entry = ttk.Entry(content_frame, textvariable=highlight_search_var)
highlight_search_entry.grid(row=4, column=3, sticky='nsew')

# --- Multi-select Listbox for Player Highlight ---
ttk.Label(content_frame, text="Highlight Player(s):").grid(row=5, column=2, sticky='ew')
highlight_player_listbox = tk.Listbox(content_frame, selectmode='multiple', exportselection=0, height=5)
highlight_player_listbox.grid(row=5, column=3, sticky='nsew', pady=2)

ttk.Button(content_frame, text="Cluster", command=lambda: plot_clusters()).grid(row=6, column=0, columnspan=4, sticky='nsew')

selected_info_var = tk.StringVar()
selected_info_label = ttk.Label(content_frame, textvariable=selected_info_var, anchor='w', justify='left', font=("Arial", 10))
selected_info_label.grid(row=7, column=0, columnspan=4, sticky='nsew', padx=5, pady=5)

def get_selected_years():
    selected = [years[i] for i in year_listbox.curselection()]
    return selected if selected else years

def get_selected_positions():
    selected = [positions[i] for i in pos_listbox.curselection()]
    return selected if selected else positions

def get_selected_players():
    return list(selected_players_set)

def get_highlight_players():
    return list(highlighted_players_set)

def update_axis_options_by_position(event=None):
    pos_selected = get_selected_positions()
    if not pos_selected or len(pos_selected) > 1:
        filtered = df
    else:
        filtered = df[df['Position'].isin(pos_selected)]
    numeric_cols = []
    for col in df.columns:
        cleaned = filtered[col].astype(str).str.replace(',', '', regex=False)
        numeric = pd.to_numeric(cleaned, errors='coerce')
        if numeric.notna().sum() > 0:
            numeric_cols.append(col)
    x_dropdown['values'] = numeric_cols
    y_dropdown['values'] = numeric_cols
    if x_var.get() not in numeric_cols and numeric_cols:
        x_var.set(numeric_cols[0])
    if y_var.get() not in numeric_cols and len(numeric_cols) > 1:
        y_var.set(numeric_cols[1])
    elif y_var.get() not in numeric_cols and numeric_cols:
        y_var.set(numeric_cols[0])

pos_listbox.bind('<<ListboxSelect>>', update_axis_options_by_position)
update_axis_options_by_position()

def rank_to_marker(rank):
    if rank <= 7:
        return '*'
    elif rank <= 16:
        return 's'
    else:
        return 'o'

def update_player_listbox(*args):
    pos_selected = get_selected_positions()
    year_selected = get_selected_years()
    search = player_search_var.get().lower()
    filtered = df.copy()
    if pos_selected:
        filtered = filtered[filtered['Position'].isin(pos_selected)]
    if year_selected:
        filtered = filtered[filtered['Year'].astype(str).isin(year_selected)]
    player_options = sorted(filtered['Player'].dropna().unique())
    if search:
        player_options = [p for p in player_options if search in p.lower()]
    player_listbox.delete(0, tk.END)
    for p in player_options:
        player_listbox.insert(tk.END, p)
    for idx, p in enumerate(player_options):
        if p in selected_players_set:
            player_listbox.selection_set(idx)

def player_search_event(event):
    update_player_listbox()
    if event.keysym == "Return":
        search = player_search_var.get().lower()
        for idx in range(player_listbox.size()):
            player = player_listbox.get(idx)
            if player.lower().startswith(search):
                player_listbox.selection_set(idx)
                selected_players_set.add(player)
                player_listbox.see(idx)
                break

def on_player_listbox_select(event):
    visible_players = [player_listbox.get(i) for i in range(player_listbox.size())]
    selected_indices = player_listbox.curselection()
    selected_players = set([player_listbox.get(i) for i in selected_indices])
    for p in visible_players:
        if p in selected_players_set and p not in selected_players:
            selected_players_set.remove(p)
    for p in selected_players:
        selected_players_set.add(p)
    update_highlight_player_listbox()  # <-- Add this line

def update_highlight_player_listbox(*args):
    pos_selected = get_selected_positions()
    year_selected = get_selected_years()
    search = highlight_search_var.get().lower()
    filtered = df.copy()
    if pos_selected:
        filtered = filtered[filtered['Position'].isin(pos_selected)]
    if year_selected:
        filtered = filtered[filtered['Year'].astype(str).isin(year_selected)]
    # If any players are selected, only show those. Otherwise, show all possible players.
    if selected_players_set:
        player_options = sorted(selected_players_set)
    else:
        player_options = sorted(filtered['Player'].dropna().unique())
    if search:
        player_options = [p for p in player_options if search in p.lower()]
    highlight_player_listbox.delete(0, tk.END)
    for p in player_options:
        highlight_player_listbox.insert(tk.END, p)
    for idx, p in enumerate(player_options):
        if p in highlighted_players_set:
            highlight_player_listbox.selection_set(idx)

def highlight_search_event(event):
    update_highlight_player_listbox()
    if event.keysym == "Return":
        search = highlight_search_var.get().lower()
        for idx in range(highlight_player_listbox.size()):
            player = highlight_player_listbox.get(idx)
            if player.lower().startswith(search):
                highlight_player_listbox.selection_set(idx)
                highlighted_players_set.add(player)
                highlight_player_listbox.see(idx)
                break

def on_highlight_listbox_select(event):
    visible_players = [highlight_player_listbox.get(i) for i in range(highlight_player_listbox.size())]
    selected_indices = highlight_player_listbox.curselection()
    selected_players = set([highlight_player_listbox.get(i) for i in selected_indices])
    for p in visible_players:
        if p in highlighted_players_set and p not in selected_players:
            highlighted_players_set.remove(p)
    for p in selected_players:
        highlighted_players_set.add(p)

def sync_global_sets_with_visible_players():
    # Sync selected_players_set
    visible_players = set([player_listbox.get(i) for i in range(player_listbox.size())])
    to_remove = set()
    for p in selected_players_set:
        if p not in visible_players:
            to_remove.add(p)
    selected_players_set.difference_update(to_remove)
    # Sync highlighted_players_set
    visible_highlight_players = set([highlight_player_listbox.get(i) for i in range(highlight_player_listbox.size())])
    to_remove_highlight = set()
    for p in highlighted_players_set:
        if p not in visible_highlight_players:
            to_remove_highlight.add(p)
    highlighted_players_set.difference_update(to_remove_highlight)

def on_year_or_pos_change(event=None):
    update_player_listbox()
    update_highlight_player_listbox()
    sync_global_sets_with_visible_players()
    plot_clusters()

def plot_clusters():
    global active_cursors, plot_canvas
    try:
        x = x_var.get()
        y = y_var.get()
        n_clusters = cluster_var.get()
        pos_selected = get_selected_positions()
        year_selected = get_selected_years()
        selected_players = get_selected_players()
        highlight_players = get_highlight_players()

        filtered = df.copy()
        # Always filter by year and position first, then by selected players
        if pos_selected:
            filtered = filtered[filtered['Position'].isin(pos_selected)]
        if year_selected:
            filtered = filtered[filtered['Year'].astype(str).isin(year_selected)]
        if selected_players:
            filtered = filtered[filtered['Player'].isin(selected_players)]

        filtered[x] = filtered[x].astype(str).str.replace(',', '', regex=False)
        filtered[y] = filtered[y].astype(str).str.replace(',', '', regex=False)
        filtered = filtered.dropna(subset=[x, y])

        try:
            filtered[x] = pd.to_numeric(filtered[x], errors='raise')
            filtered[y] = pd.to_numeric(filtered[y], errors='raise')
        except Exception:
            tk.messagebox.showerror(
                "Invalid Axis Selection",
                f"Selected axis columns must be numeric.\nYou chose:\nX: {x}\nY: {y}"
            )
            return

        X = filtered[[x, y]].astype(float).to_numpy()

        plt.close('all')
        if filtered.empty:
            fig, ax = plt.subplots()
            ax.text(0.5, 0.5, f'No data for selection\n(0 records matched)', ha='center', va='center')
            ax.set_axis_off()
        else:
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            kmeans = KMeans(n_clusters=n_clusters, n_init=10, random_state=42)
            clusters = kmeans.fit_predict(X_scaled)
            filtered['Cluster'] = clusters

            colors = plt.cm.get_cmap('tab10', n_clusters)
            fig, ax = plt.subplots()
            for i in range(n_clusters):
                group = filtered[filtered['Cluster'] == i]
                for marker, marker_group in group.groupby(group['Rank'].apply(rank_to_marker)):
                    ax.scatter(
                        marker_group[x],
                        marker_group[y],
                        label=f'Cluster {i+1} ({marker})' if marker == '*' else None,
                        color=colors(i),
                        alpha=0.6,
                        s=30,
                        marker=marker
                    )
            if highlight_players:
                highlight_df = filtered[filtered['Player'].isin(highlight_players)]
                if not highlight_df.empty:
                    ax.scatter(
                        highlight_df[x],
                        highlight_df[y],
                        s=120,
                        facecolors='none',
                        edgecolors='black',
                        linewidths=2,
                        label='Highlighted Player(s)',
                        zorder=10
                    )
            centers = scaler.inverse_transform(kmeans.cluster_centers_)
            ax.scatter(centers[:, 0], centers[:, 1], c='black', marker='x', s=60, linewidths=2, label='Centers')

            ax.set_xlabel(x)
            ax.set_ylabel(y)
            ax.set_title(f'KMeans Clustering: {y} vs {x}')
            ax.legend()

            x_vals = filtered[x].astype(float).values
            y_vals = filtered[y].astype(float).values
            center_x = centers[:, 0]
            center_y = centers[:, 1]
            all_x = np.concatenate([x_vals, center_x])
            all_y = np.concatenate([y_vals, center_y])

            x_min = np.nanmin(all_x)
            x_max = np.nanmax(all_x)
            y_min = np.nanmin(all_y)
            y_max = np.nanmax(all_y)
            x_margin = (x_max - x_min) * 0.05 if x_max > x_min else 1
            y_margin = (y_max - y_min) * 0.05 if y_max > y_min else 1
            x_lower, x_upper = sorted([x_min - x_margin, x_max + x_margin])
            y_lower, y_upper = sorted([y_min - y_margin, y_max + y_margin])

            ax.set_xlim(x_lower, x_upper)
            ax.set_ylim(y_lower, y_upper)

            if ax.get_xlim()[0] > ax.get_xlim()[1]:
                ax.invert_xaxis()
            if ax.get_ylim()[0] > ax.get_ylim()[1]:
                ax.invert_yaxis()

            ax.tick_params(axis='x', labelrotation=45)
            ax.tick_params(axis='y', labelrotation=0)
            fig.tight_layout()

            active_cursors = []
            sc = ax.scatter(filtered[x], filtered[y], c=filtered['Cluster'], cmap='tab10', alpha=0)
            cursor = mplcursors.cursor(sc, hover=False)
            active_cursors.append(cursor)
            @cursor.connect("add")
            def on_add(sel):
                idx = sel.index
                player = filtered.iloc[idx]['Player']
                year_val = filtered.iloc[idx]['Year']
                cluster = filtered.iloc[idx]['Cluster']
                x_val = filtered.iloc[idx][x]
                y_val = filtered.iloc[idx][y]
                rank = filtered.iloc[idx]['Rank'] if 'Rank' in filtered.columns else 'N/A'
                text = (
                    f"{player} ({year_val})\n"
                    f"Cluster: {cluster+1}\n"
                    f"Fantasy Rank: {int(rank) if pd.notnull(rank) else 'N/A'}\n"
                    f"{x}: {x_val}\n"
                    f"{y}: {y_val}"
                )
                sel.annotation.set(text=text)
                selected_info_var.set(text)

        if plot_canvas is not None:
            plot_canvas.get_tk_widget().destroy()
        plot_canvas_new = FigureCanvasTkAgg(fig, master=content_frame)
        plot_canvas_new.get_tk_widget().grid(row=8, column=0, columnspan=4, sticky='nsew')
        # Remove fixed width/height to allow expansion
        plot_canvas_new.draw()
        plot_canvas = plot_canvas_new
    except Exception as e:
        import traceback
        print("Exception in plot_clusters():", e)
        traceback.print_exc()

# Make only the plot row expandable
for i in range(8):
    content_frame.rowconfigure(i, weight=0)
content_frame.rowconfigure(8, weight=1)

for i in range(4):
    content_frame.columnconfigure(i, weight=1)

plot_clusters()

year_listbox.bind('<<ListboxSelect>>', on_year_or_pos_change)
pos_listbox.bind('<<ListboxSelect>>', on_year_or_pos_change)
player_search_entry.bind('<KeyRelease>', player_search_event)
player_listbox.bind('<<ListboxSelect>>', on_player_listbox_select)
highlight_search_entry.bind('<KeyRelease>', highlight_search_event)
highlight_player_listbox.bind('<<ListboxSelect>>', on_highlight_listbox_select)

update_player_listbox()
update_highlight_player_listbox()

window.mainloop()





















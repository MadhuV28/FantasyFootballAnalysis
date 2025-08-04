import pandas as pd
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import mplcursors
import matplotlib
import numpy as np
matplotlib.use('TkAgg')

# Load the data
df = pd.read_csv('/Users/mvuyyuru/FantasyAnalyticsProject/DataInfo/2025_ADP_VORP.csv')

# Clean up columns for plotting
df = df[['Rank', 'Player', 'Team', 'POS', 'AVG', 'VORP', 'VORPvsADP']].copy()

# Group POS (e.g., TE1, TE2 -> TE)
def group_pos(pos):
    pos = str(pos).upper()
    for prefix in ['QB', 'RB', 'WR', 'TE', 'DST', 'K']:
        if pos.startswith(prefix):
            return prefix
    return pos
df['POS_GROUP'] = df['POS'].apply(group_pos)

# Clean numeric columns
for col in ['AVG', 'VORP']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Clean VORPvsADP (remove +, spaces, convert to float)
def clean_vorp_vs_adp(val):
    if pd.isnull(val):
        return np.nan
    val = str(val).replace('+', '').replace(' ', '')
    try:
        return float(val)
    except:
        return np.nan
df['VORPvsADP_clean'] = df['VORPvsADP'].apply(clean_vorp_vs_adp)

# Prepare GUI
window = tk.Tk()
window.title("2025 ADP VORP Analysis")
window.geometry("1100x800")
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
for i in range(8):
    content_frame.rowconfigure(i, weight=1)

# Filtering options
positions = ['QB', 'RB', 'WR', 'TE', 'DST', 'K']

# Position filter
ttk.Label(content_frame, text="Position(s):").grid(row=0, column=0, sticky='ew')
pos_frame = ttk.Frame(content_frame)
pos_frame.grid(row=0, column=1, sticky='nsew', pady=2)
pos_listbox = tk.Listbox(pos_frame, selectmode='multiple', exportselection=0, height=3)
pos_scroll = ttk.Scrollbar(pos_frame, orient="vertical", command=pos_listbox.yview)
pos_listbox.configure(yscrollcommand=pos_scroll.set)
pos_listbox.pack(side="left", fill="both", expand=True)
pos_scroll.pack(side="right", fill="y")
for p in positions:
    pos_listbox.insert(tk.END, p)

def on_position_select(event):
    update_player_listbox()
    update_highlight_player_listbox()
    plot()

# Bind position selection to update player/highlight lists and plot
pos_listbox.bind("<<ListboxSelect>>", on_position_select)

# Player search and selection
player_search_var = tk.StringVar()
ttk.Label(content_frame, text="Search Player:").grid(row=1, column=0, sticky='ew')
player_search_entry = ttk.Entry(content_frame, textvariable=player_search_var)
player_search_entry.grid(row=1, column=1, sticky='nsew')

ttk.Label(content_frame, text="Player(s):").grid(row=2, column=0, sticky='ew')
player_listbox = tk.Listbox(content_frame, selectmode='multiple', exportselection=0, height=5)
player_listbox.grid(row=2, column=1, sticky='nsew', pady=2)

highlight_search_var = tk.StringVar()
ttk.Label(content_frame, text="Search Highlight:").grid(row=1, column=2, sticky='ew')
highlight_search_entry = ttk.Entry(content_frame, textvariable=highlight_search_var)
highlight_search_entry.grid(row=1, column=3, sticky='nsew')

ttk.Label(content_frame, text="Highlight Player(s):").grid(row=2, column=2, sticky='ew')
highlight_player_listbox = tk.Listbox(content_frame, selectmode='multiple', exportselection=0, height=5)
highlight_player_listbox.grid(row=2, column=3, sticky='nsew', pady=2)

# Axis selection
axis_options = ['AVG', 'VORP', 'VORPvsADP_clean']
axis_labels = {'AVG': 'ADP AVG', 'VORP': 'VORP', 'VORPvsADP_clean': 'VORP vs ADP'}

x_var = tk.StringVar(value='AVG')
ttk.Label(content_frame, text="X Axis:").grid(row=3, column=0, sticky='ew')
x_dropdown = ttk.Combobox(content_frame, textvariable=x_var, values=[axis_labels[a] for a in axis_options])
x_dropdown.grid(row=3, column=1, sticky='nsew')

y_var = tk.StringVar(value='VORP')
ttk.Label(content_frame, text="Y Axis:").grid(row=4, column=0, sticky='ew')
y_dropdown = ttk.Combobox(content_frame, textvariable=y_var, values=[axis_labels[a] for a in axis_options])
y_dropdown.grid(row=4, column=1, sticky='nsew')

ttk.Button(content_frame, text="Plot", command=lambda: plot()).grid(row=5, column=0, columnspan=4, sticky='nsew')

selected_info_var = tk.StringVar()
selected_info_label = ttk.Label(content_frame, textvariable=selected_info_var, anchor='w', justify='left', font=("Arial", 10))
selected_info_label.grid(row=6, column=0, columnspan=4, sticky='nsew', padx=5, pady=5)

active_cursors = []
plot_canvas = None
highlighted_players_set = set()
selected_players_set = set()

def get_selected_positions():
    selected = [positions[i] for i in pos_listbox.curselection()]
    return selected if selected else positions

def get_selected_players():
    return list(selected_players_set)

def get_highlight_players():
    return list(highlighted_players_set)

def update_player_listbox(*args):
    pos_selected = get_selected_positions()
    search = player_search_var.get().lower()
    filtered = df[df['POS_GROUP'].isin(pos_selected)]
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
    update_highlight_player_listbox()

def update_highlight_player_listbox(*args):
    pos_selected = get_selected_positions()
    search = highlight_search_var.get().lower()
    filtered = df[df['POS_GROUP'].isin(pos_selected)]
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

def plot():
    global active_cursors, plot_canvas
    try:
        for cursor in active_cursors:
            try:
                cursor.remove()
            except Exception:
                pass
        active_cursors = []

        # Axis mapping
        axis_map = {v: k for k, v in axis_labels.items()}
        x = axis_map.get(x_var.get(), 'AVG')
        y = axis_map.get(y_var.get(), 'VORP')

        pos_selected = get_selected_positions()
        selected_players = get_selected_players()
        highlight_players = get_highlight_players()

        # Filter by position and ADP <= 300
        filtered = df[(df['POS_GROUP'].isin(pos_selected)) & (df['AVG'] <= 300)]
        if selected_players:
            filtered = filtered[filtered['Player'].isin(selected_players)]

        filtered = filtered.dropna(subset=[x, y])

        plt.close('all')
        if filtered.empty:
            fig, ax = plt.subplots()
            ax.text(0.5, 0.5, f'No data for selection\n(0 records matched)', ha='center', va='center')
            ax.set_axis_off()
        else:
            fig, ax = plt.subplots()
            ax.text(0.01, 0.99, f'{len(filtered)} records matched', ha='left', va='top', fontsize=8, transform=ax.transAxes)
            filtered = filtered.reset_index(drop=True)
            color_map = {'RB': 'green', 'WR': 'blue', 'TE': 'orange', 'QB': 'red', 'K': 'purple', 'DST': 'gray'}
            scatter_objs = []
            for pos in pos_selected:
                group_data = filtered[filtered['POS_GROUP'] == pos]
                if not group_data.empty:
                    sc = ax.scatter(group_data[x], group_data[y], label=pos, color=color_map.get(pos, 'black'), alpha=0.6, s=30)
                    scatter_objs.append((sc, group_data))
            # Regression line if numeric
            if (
                len(filtered) > 1
                and pd.api.types.is_numeric_dtype(filtered[x])
                and pd.api.types.is_numeric_dtype(filtered[y])
                and filtered[x].nunique() > 1
                and filtered[y].nunique() > 1
            ):
                z = np.polyfit(filtered[x], filtered[y], 1)
                p = np.poly1d(z)
                ax.plot(filtered[x], p(filtered[x]), "k--")
            ax.set_xlabel(axis_labels[x])
            ax.set_ylabel(axis_labels[y])
            ax.set_title(f'{axis_labels[y]} vs {axis_labels[x]}')
            active_cursors = []

            for sc, group_data in scatter_objs:
                cursor = mplcursors.cursor(sc, hover=False)
                active_cursors.append(cursor)
                @cursor.connect("add")
                def on_add(sel, group_data=group_data):
                    idx = sel.index
                    player = group_data.iloc[idx]['Player']
                    pos = group_data.iloc[idx]['POS']
                    team = group_data.iloc[idx]['Team']
                    x_val = group_data.iloc[idx][x]
                    y_val = group_data.iloc[idx][y]
                    text = f"{player} ({pos}, {team})\n{x_var.get()}: {x_val}\n{y_var.get()}: {y_val}"
                    sel.annotation.set_text(text)
                    sel.annotation.get_bbox_patch().set_alpha(0.8)
                    sel.annotation.get_bbox_patch().set_facecolor('lightyellow')
                    sel.annotation.get_bbox_patch().set_edgecolor('black')
                    sel.annotation.set_fontsize(10)
                    sel.annotation.set_horizontalalignment('center')
                    sel.annotation.set_verticalalignment('center')
                    return sel

        # Update plot area in GUI
        if plot_canvas is not None:
            plot_canvas.get_tk_widget().destroy()
        plot_canvas = FigureCanvasTkAgg(fig, master=content_frame)
        plot_canvas.draw()
        plot_canvas.get_tk_widget().grid(row=7, column=0, columnspan=4, sticky='nsew')

        # Update selected info
        if not filtered.empty:
            first_player = filtered.iloc[0]['Player']
            first_pos = filtered.iloc[0]['POS']
            first_team = filtered.iloc[0]['Team']
            first_x_val = filtered.iloc[0][x]
            first_y_val = filtered.iloc[0][y]
            selected_info_var.set(f"First Player: {first_player} ({first_pos}, {first_team}) - {x_var.get()}: {first_x_val}, {y_var.get()}: {first_y_val}")
        else:
            selected_info_var.set("No data to display")

    except Exception as e:
        print(f"Error in plot: {e}")

# Bind events
player_search_entry.bind("<KeyRelease>", player_search_event)
player_listbox.bind("<<ListboxSelect>>", on_player_listbox_select)
highlight_search_entry.bind("<KeyRelease>", highlight_search_event)
highlight_player_listbox.bind("<<ListboxSelect>>", on_highlight_listbox_select)

update_player_listbox()
update_highlight_player_listbox()
plot()

window.mainloop()
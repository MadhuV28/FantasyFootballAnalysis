import pandas as pd
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import mplcursors
import os
import matplotlib
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
active_crosshairs = []
plot_canvas = None

highlighted_players_set = set()
selected_players_set = set()

window = tk.Tk()
window.title("Fantasy Analytics Plotter")
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

# --- Player and Highlight Player UI ---
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

x_var = tk.StringVar(value=columns[0])
ttk.Label(content_frame, text="X Axis:").grid(row=3, column=0, sticky='ew')
x_entry = ttk.Entry(content_frame, textvariable=x_var)
x_entry.grid(row=3, column=1, sticky='nsew')
x_dropdown = ttk.Combobox(content_frame, textvariable=x_var, values=columns)
x_dropdown.grid(row=3, column=2, sticky='nsew')
x_dropdown.label_to_col = {}

y_var = tk.StringVar(value=columns[1])
ttk.Label(content_frame, text="Y Axis:").grid(row=4, column=0, sticky='ew')
y_entry = ttk.Entry(content_frame, textvariable=y_var)
y_entry.grid(row=4, column=1, sticky='nsew')
y_dropdown = ttk.Combobox(content_frame, textvariable=y_var, values=columns)
y_dropdown.grid(row=4, column=2, sticky='nsew')
y_dropdown.label_to_col = {}

ttk.Button(content_frame, text="Plot", command=lambda: plot()).grid(row=5, column=0, columnspan=4, sticky='nsew')

selected_info_var = tk.StringVar()
selected_info_label = ttk.Label(content_frame, textvariable=selected_info_var, anchor='w', justify='left', font=("Arial", 10))
selected_info_label.grid(row=6, column=0, columnspan=4, sticky='nsew', padx=5, pady=5)

# --- Feature correlation for axis dropdowns ---
correlation_dir = '/Users/mvuyyuru/FantasyAnalyticsProject/scripts/ModelingAnalysis/PosSpecific'
correlation_files = {
    'QB': 'QB_feature_correlations.csv',
    'RB': 'RB_feature_correlations.csv',
    'WR': 'WR_feature_correlations.csv',
    'TE': 'TE_feature_correlations.csv'
}
feature_correlations = {}
for pos, fname in correlation_files.items():
    path = os.path.join(correlation_dir, fname)
    if os.path.exists(path):
        corr_df = pd.read_csv(path, index_col=0)
        feature_correlations[pos] = corr_df['Fantasy Points'].to_dict()
    else:
        feature_correlations[pos] = {}

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

def update_axis_options(event, axis_var, entry, dropdown, columns):
    label_to_col = dropdown.label_to_col if hasattr(dropdown, 'label_to_col') else {col: col for col in columns}
    typed = entry.get().lower()
    matches = [label for label in label_to_col if typed in label.lower()]
    dropdown['values'] = matches if matches else list(label_to_col.keys())
    if event.keysym == "Return" and matches:
        axis_var.set(matches[0])

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

def update_axis_choices(*args):
    pos_selected = get_selected_positions()
    if not pos_selected or len(pos_selected) != 1:
        filtered = df
        correlations = {}
        valid_columns = sorted([col for col in df.columns if filtered[col].notna().any()])
    else:
        filtered = df[df['Position'].isin(pos_selected)]
        correlations = feature_correlations.get(pos_selected[0], {})
        valid_columns = [col for col in df.columns if filtered[col].notna().any()]
        valid_columns.sort(key=lambda col: (-(correlations.get(col, float('-inf')) if isinstance(correlations.get(col), float) else float('-inf')), col))
    label_to_col = {}
    labels = []
    for col in valid_columns:
        corr = correlations.get(col, None)
        if isinstance(corr, float):
            label = f"{col} (corr={corr:.2f})"
        elif corr is not None and corr != 'n/a':
            label = f"{col} (corr={corr})"
        else:
            label = f"{col}"
        label_to_col[label] = col
        labels.append(label)
    x_dropdown.label_to_col = label_to_col
    y_dropdown.label_to_col = label_to_col
    x_dropdown['values'] = labels
    y_dropdown['values'] = labels

    if x_var.get() not in labels and labels:
        x_var.set(labels[0])
    if y_var.get() not in labels and len(labels) > 1:
        y_var.set(labels[1])
    elif y_var.get() not in labels and labels:
        y_var.set(labels[0])

def on_year_or_pos_change(event=None):
    update_player_listbox()
    update_highlight_player_listbox()
    update_axis_choices()
    plot()

year_listbox.bind('<<ListboxSelect>>', on_year_or_pos_change)
pos_listbox.bind('<<ListboxSelect>>', on_year_or_pos_change)
player_search_entry.bind('<KeyRelease>', player_search_event)
player_listbox.bind('<<ListboxSelect>>', on_player_listbox_select)
highlight_search_entry.bind('<KeyRelease>', highlight_search_event)
highlight_player_listbox.bind('<<ListboxSelect>>', on_highlight_listbox_select)

update_player_listbox()
update_highlight_player_listbox()
update_axis_choices()

def plot():
    global active_cursors, active_crosshairs, plot_canvas
    try:
        for cursor in active_cursors:
            try:
                cursor.remove()
            except Exception:
                pass
        active_cursors = []
        for line in active_crosshairs:
            try:
                line.remove()
            except Exception:
                pass
        active_crosshairs = []

        x_label = x_var.get()
        y_label = y_var.get()
        x = x_dropdown.label_to_col.get(x_label, x_label)
        y = y_dropdown.label_to_col.get(y_label, y_label)

        pos_selected = get_selected_positions()
        year_selected = get_selected_years()
        selected_players = get_selected_players()
        highlight_players = get_highlight_players()

        filtered = df.copy()
        if pos_selected:
            filtered = filtered[filtered['Position'].isin(pos_selected)]
        if year_selected:
            filtered = filtered[filtered['Year'].astype(str).isin(year_selected)]
        if selected_players:
            filtered = filtered[filtered['Player'].isin(selected_players)]

        cols = list({x, y, 'Fantasy Points', 'Year', 'Player', 'Rank', 'Group'})
        if 'Team' in filtered.columns:
            cols.append('Team')
        numeric_cols = [col for col in [x, y, 'Fantasy Points', 'Year', 'Rank'] if col in cols]
        string_cols = [col for col in ['Player', 'Team', 'Group'] if col in cols]
        filtered_numeric = filtered[numeric_cols].apply(pd.to_numeric, errors='coerce', downcast='float')
        filtered_strings = filtered[string_cols]
        filtered = pd.concat([filtered_numeric, filtered_strings], axis=1)
        filtered = filtered.loc[:,~filtered.columns.duplicated()]
        filtered = filtered.dropna(subset=[x, y, 'Fantasy Points', 'Year'])

        plt.close('all')
        if filtered.empty:
            fig, ax = plt.subplots()
            ax.text(0.5, 0.5, f'No data for selection\n(0 records matched)', ha='center', va='center')
            ax.set_axis_off()
        else:
            fig, ax = plt.subplots()
            ax.text(0.01, 0.99, f'{len(filtered)} records matched', ha='left', va='top', fontsize=8, transform=ax.transAxes)
            filtered = filtered.reset_index(drop=True)
            color_map = {'Top 5': 'red', '6-10': 'orange', '11-20': 'green', '21+': 'blue'}
            scatter_objs = []
            for group, color in color_map.items():
                group_data = filtered[filtered['Group'] == group]
                sc = ax.scatter(group_data[x], group_data[y], label=group, color=color, alpha=0.5, s=20)
                scatter_objs.append((sc, group_data))
            import numpy as np
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
            ax.set_xlabel(x)
            ax.set_ylabel(y)
            ax.set_title(f'{y} vs {x}')
            active_crosshairs = []
            active_cursors = []

            for sc, group_data in scatter_objs:
                cursor = mplcursors.cursor(sc, hover=False)
                active_cursors.append(cursor)
                @cursor.connect("add")
                def on_add(sel, group_data=group_data):
                    if hasattr(sel.annotation, "crosshair_lines"):
                        for line in sel.annotation.crosshair_lines:
                            try:
                                line.remove()
                            except Exception:
                                pass
                        sel.annotation.crosshair_lines = []

                    idx = sel.index
                    player = group_data.iloc[idx]['Player']
                    year_val = int(group_data.iloc[idx]['Year'])
                    rank = int(group_data.iloc[idx]['Rank'])
                    x_val = group_data.iloc[idx][x]
                    y_val = group_data.iloc[idx][y]
                    text = f"{player} ({year_val})\nFantasy Rank: {rank}"
                    if 'Team' in group_data.columns:
                        team = group_data.iloc[idx]['Team']
                        text += f"\nTeam: {team}"
                    text += f"\n{x}: {x_val}\n{y}: {y_val}"
                    if highlight_players and player in highlight_players:
                        text += "\n[HIGHLIGHTED]"
                    sel.annotation.set(text=text)
                    selected_info_var.set(text)
                    ax = sel.artist.axes
                    vline = ax.axvline(x=x_val, color='gray', linestyle='dotted', linewidth=1)
                    hline = ax.axhline(y_val, color='gray', linestyle='dotted', linewidth=1)
                    sel.annotation.crosshair_lines = [vline, hline]

                @cursor.connect("remove")
                def on_remove(sel):
                    if hasattr(sel.annotation, "crosshair_lines"):
                        for line in sel.annotation.crosshair_lines:
                            try:
                                line.remove()
                            except Exception:
                                pass
                        sel.annotation.crosshair_lines = []

            # Highlight selected players
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

            def hide_annotation_on_motion(event):
                redraw = False
                for cursor in active_cursors:
                    for annotation in getattr(cursor, 'annotations', []):
                        vis = annotation.get_visible()
                        contains, _ = annotation.contains(event)
                        if vis and not contains:
                            annotation.set_visible(False)
                            redraw = True
                if redraw:
                    fig.canvas.draw_idle()

            def hide_all_annotations(event):
                redraw = False
                for cursor in active_cursors:
                    for annotation in getattr(cursor, 'annotations', []):
                        if annotation.get_visible():
                            annotation.set_visible(False)
                            redraw = True
                if redraw:
                    fig.canvas.draw_idle()

            fig.canvas.mpl_connect('motion_notify_event', hide_annotation_on_motion)
            fig.canvas.mpl_connect('figure_leave_event', hide_all_annotations)
            fig.canvas.mpl_connect('axes_leave_event', hide_all_annotations)

        if plot_canvas is not None:
            plot_canvas.get_tk_widget().destroy()
        plot_canvas_new = FigureCanvasTkAgg(fig, master=content_frame)
        plot_canvas_new.get_tk_widget().grid(row=8, column=0, columnspan=4, sticky='nsew')
        plot_canvas_new.draw()
        plot_canvas = plot_canvas_new
    except Exception as e:
        import traceback
        print("Exception in plot():", e)
        traceback.print_exc()

# Only the plot row expands


plot()
window.mainloop()




import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random
from player_pool import load_player_pool
from team import Team

class DraftSimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Fantasy Draft Simulator")

        # Mode selection
        self.mode = self.ask_mode()
        if self.mode is None:
            self.root.destroy()
            return

        # Draft setup
        self.NUM_TEAMS = 12
        self.ROUNDS = 16
        self.roster_requirements = {
            "QB": 1, "RB": 2, "WR": 2, "TE": 1, "FLEX": 1, "DST": 1, "K": 1, "BENCH": 6
        }
        self.player_pool = load_player_pool().to_dict('records')
        self.teams = [Team(f"Team {i+1}", self.roster_requirements) for i in range(self.NUM_TEAMS)]
        self.user_team_idx = random.randint(0, self.NUM_TEAMS - 1)
        self.draft_order = list(range(self.NUM_TEAMS))
        self.recent_picks = []
        self.RUN_WINDOW = 8
        self.draft_log = []
        self.round_num = 1
        self.pick_idx = 0
        self.user_done = False

        # Tkinter Notebook (tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)

        # Tab 1: Best available
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="Best Available")
        self.best_avail_list = tk.Listbox(self.tab1, width=60, height=20)
        self.best_avail_list.pack(pady=10)
        self.recommend_label = tk.Label(self.tab1, text="", font=("Arial", 12, "bold"))
        self.recommend_label.pack()
        self.pick_button = tk.Button(self.tab1, text="Draft Selected Player", command=self.user_pick)
        self.pick_button.pack(pady=10)

        # Tab 2: Draft history
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text="Draft History")
        self.history_text = tk.Text(self.tab2, width=70, height=25, state='disabled')
        self.history_text.pack(padx=10, pady=10)

        # Tab 3: User team
        self.tab3 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab3, text="Your Team")
        self.user_team_text = tk.Text(self.tab3, width=40, height=25, state='disabled')
        self.user_team_text.pack(padx=10, pady=10)

        # Start draft
        self.update_tabs()
        self.root.after(500, self.draft_loop)

    def ask_mode(self):
        mode = None
        def set_mode(val):
            nonlocal mode
            mode = val
            popup.destroy()
        popup = tk.Toplevel(self.root)
        popup.title("Select Draft Mode")
        tk.Label(popup, text="Select Draft Mode:", font=("Arial", 14)).pack(padx=20, pady=10)
        tk.Button(popup, text="1. Standard (CPU picks for other teams)", width=40, command=lambda: set_mode(1)).pack(pady=5)
        tk.Button(popup, text="2. Manual (You pick for ALL teams)", width=40, command=lambda: set_mode(2)).pack(pady=5)
        popup.grab_set()
        self.root.wait_window(popup)
        return mode

    def cpu_pick(self, team, player_pool, recent_picks, round_num=1):
        needs = team.needs()
        scores = []
        run_counts = {}
        for pos, _ in recent_picks:
            base_pos = ''.join([c for c in pos if not c.isdigit()])
            run_counts[base_pos] = run_counts.get(base_pos, 0) + 1
        rb_count = sum(1 for p in team.roster if 'RB' in p['POS'])

        for i, player in enumerate(player_pool[:30]):
            pos = ''.join([c for c in player['POS'] if not c.isdigit()])
            score = 0

            # --- Early rounds: strongly favor WR, fade RB ---
            if round_num <= 3:
                if pos == 'RB':
                    score -= 15  # Penalize RBs in first 3 rounds
                    if rb_count >= 1:
                        score -= 100  # Never double-tap RB early
                if pos == 'WR':
                    score += 15   # Strongly favor WRs early
                if pos in ['QB', 'TE'] and i < 5:
                    score += 5    # Slightly favor elite QB/TE
                # NO team need bonus in first 3 rounds!
            else:
                # After round 3, only a gentle nudge for team need (except RB)
                if pos == 'RB':
                    score -= 2  # Still fade RBs a bit
                elif needs.get(pos, 0) > 0 or (pos in ['WR', 'TE'] and needs.get('FLEX', 0) > 0):
                    score += 3

            # Rankings/VORP/ADP is the main driver
            try:
                vorp = float(player.get('VORP', 0))
            except:
                vorp = 0
            score += vorp

            # Scarcity: tiny boost
            same_pos_players = [p for p in player_pool if ''.join([c for c in p['POS'] if not c.isdigit()]) == pos]
            if len(same_pos_players) > 1:
                try:
                    next_vorp = float(same_pos_players[1].get('VORP', 0))
                except:
                    next_vorp = 0
                if vorp - next_vorp > 15:
                    score += 1

            # Run awareness: tiny boost
            if run_counts.get(pos, 0) >= 3:
                score += 1

            # Small randomness for realism
            score += random.uniform(-1, 1)

            if team.can_add_player(player):
                scores.append((score, i, player))
        if scores:
            scores.sort(reverse=True)
            _, pick_idx, pick_player = scores[0]
            return player_pool.pop(pick_idx)
        for i, player in enumerate(player_pool):
            if team.can_add_player(player):
                return player_pool.pop(i)
        return player_pool.pop(0)

    def recommend_pick(self, team, player_pool):
        needs = team.needs()
        for player in player_pool:
            pos = ''.join([c for c in player['POS'] if not c.isdigit()])
            if team.can_add_player(player):
                if needs.get(pos, 0) > 0 or (pos in ['RB', 'WR', 'TE'] and needs.get('FLEX', 0) > 0):
                    return player
        for player in player_pool:
            if team.can_add_player(player):
                return player
        return None

    def update_tabs(self):
        # Tab 1: Best available
        self.best_avail_list.delete(0, tk.END)
        # Determine which team is up
        if self.mode == 2:
            team_idx = self.draft_order[self.pick_idx % self.NUM_TEAMS]
            user_team = self.teams[team_idx]
        else:
            user_team = self.teams[self.user_team_idx]
        available_choices = [p for p in self.player_pool if user_team.can_add_player(p)]
        for i, p in enumerate(available_choices[:20]):
            self.best_avail_list.insert(tk.END, f"{i+1}. {p['Player']} ({p['POS']})")
        recommended = self.recommend_pick(user_team, self.player_pool)
        if recommended:
            self.recommend_label.config(text=f"Recommended: {recommended['Player']} ({recommended['POS']})")
        else:
            self.recommend_label.config(text="No recommendation (roster full or no valid picks left)")

        # Tab 2: Draft history
        self.history_text.config(state='normal')
        self.history_text.delete(1.0, tk.END)
        for rnd, picks in enumerate(self.draft_log):
            self.history_text.insert(tk.END, f"--- Round {rnd+1} ---\n")
            for player_name, pos, idx in picks:
                self.history_text.insert(tk.END, f"Team {idx+1}: {player_name} ({pos})\n")
            self.history_text.insert(tk.END, "\n")
        self.history_text.config(state='disabled')

        # Tab 3: User team
        self.user_team_text.config(state='normal')
        self.user_team_text.delete(1.0, tk.END)
        for p in self.teams[self.user_team_idx].roster:
            self.user_team_text.insert(tk.END, f"{p['Player']} ({p['POS']})\n")
        self.user_team_text.config(state='disabled')

    def user_pick(self):
        # In manual mode, pick for current team; otherwise, pick for user team only
        if self.mode == 2:
            team_idx = self.draft_order[self.pick_idx % self.NUM_TEAMS]
            team = self.teams[team_idx]
        else:
            team_idx = self.user_team_idx
            team = self.teams[self.user_team_idx]
        available_choices = [p for p in self.player_pool if team.can_add_player(p)]
        selection = self.best_avail_list.curselection()
        if not available_choices or not selection:
            messagebox.showinfo("No Pick", "No available players or no player selected.")
            return
        idx = selection[0]
        player = available_choices[idx]
        team.add_player(player)
        self.player_pool.remove(player)
        self.recent_picks.append((player['POS'], team_idx))
        if len(self.recent_picks) > self.RUN_WINDOW:
            self.recent_picks.pop(0)
        if len(self.draft_log) < self.round_num:
            self.draft_log.append([])
        self.draft_log[self.round_num-1].append((player['Player'], player['POS'], team_idx))
        self.pick_idx += 1
        self.update_tabs()
        self.root.after(500, self.draft_loop)

    def draft_loop(self):
        if self.mode == 2:
            # Manual mode: always wait for user pick for every team
            self.update_tabs()
            return
        # Standard mode: user picks for their team, CPU for others
        if self.pick_idx % self.NUM_TEAMS == self.user_team_idx:
            self.update_tabs()
            return
        # CPU pick
        idx = self.draft_order[self.pick_idx % self.NUM_TEAMS]
        if idx == self.user_team_idx:
            self.update_tabs()
            return
        team = self.teams[idx]
        player = self.cpu_pick(team, self.player_pool, self.recent_picks, round_num=self.round_num)
        team.add_player(player)
        self.recent_picks.append((player['POS'], idx))
        if len(self.recent_picks) > self.RUN_WINDOW:
            self.recent_picks.pop(0)
        if len(self.draft_log) < self.round_num:
            self.draft_log.append([])
        self.draft_log[self.round_num-1].append((player['Player'], player['POS'], idx))
        self.pick_idx += 1
        if self.pick_idx % self.NUM_TEAMS == 0:
            # End of round
            self.round_num += 1
            self.draft_order.reverse()
        self.update_tabs()
        if self.round_num <= self.ROUNDS and self.pick_idx < self.NUM_TEAMS * self.ROUNDS:
            self.root.after(500, self.draft_loop)
        else:
            messagebox.showinfo("Draft Complete", "Draft is complete! Check your team and draft history.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DraftSimulatorGUI(root)
    root.mainloop()
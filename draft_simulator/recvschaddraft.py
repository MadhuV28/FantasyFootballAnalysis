import pandas as pd
import os
from player_pool import load_player_pool

# --- Team and recommend_pick logic (reuse from your simulator) ---
class Team:
    def __init__(self, name, requirements):
        self.name = name
        self.requirements = requirements.copy()
        self.roster = []
        self.counts = {pos: 0 for pos in requirements}

    def needs(self):
        needs = {}
        for pos, req in self.requirements.items():
            needs[pos] = max(0, req - self.counts.get(pos, 0))
        return needs

    def can_add_player(self, player):
        pos = ''.join([c for c in player['POS'] if not c.isdigit()])
        needs = self.needs()
        if needs.get(pos, 0) > 0:
            return True
        if pos in ['RB', 'WR', 'TE'] and needs.get('FLEX', 0) > 0:
            return True
        if needs.get('BENCH', 0) > 0:
            return True
        return False

    def add_player(self, player):
        pos = ''.join([c for c in player['POS'] if not c.isdigit()])
        self.roster.append(player)
        if self.counts.get(pos) is not None:
            self.counts[pos] += 1
        elif pos in ['RB', 'WR', 'TE'] and self.counts.get('FLEX') is not None and self.counts['FLEX'] < self.requirements['FLEX']:
            self.counts['FLEX'] += 1
        else:
            self.counts['BENCH'] += 1

def recommend_pick(team, player_pool):
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

def get_top_n_recommendations(team, player_pool, n=5):
    recs = []
    pool_copy = player_pool.copy()
    for _ in range(n):
        rec = recommend_pick(team, pool_copy)
        if rec:
            recs.append(rec)
            pool_copy.remove(rec)
        else:
            break
    return recs

def normalize(name):
    return name.strip().lower()

def find_player_by_name(name, player_pool):
    norm_name = normalize(name)
    for p in player_pool:
        if normalize(p['Player']) == norm_name:
            return p
    return None

def main():
    NUM_TEAMS = 12
    ROUNDS = 16
    roster_requirements = {
        "QB": 1, "RB": 2, "WR": 2, "TE": 1, "FLEX": 1, "DST": 1, "K": 1, "BENCH": 6
    }
    # Load player pool
    player_pool_df = load_player_pool()
    player_pool = player_pool_df.to_dict('records')

    # Load draft order CSV (tab-delimited)
    draft_order_path = os.path.join(os.path.dirname(__file__), "data", "2025ChadDraft.csv")
    draft_df = pd.read_csv(draft_order_path, delimiter='\t')
    draft_df['Round'] = draft_df['Round'].astype(int)

    # Build draft rounds as list of lists (each round is a list of player names)
    draft_rounds = []
    for rnd in range(1, ROUNDS+1):
        round_picks = draft_df[draft_df['Round'] == rnd]['Player'].tolist()
        draft_rounds.append(round_picks)

    # --- Simulate Actual Draft ---
    teams_actual = [Team(f"Team {i+1}", roster_requirements) for i in range(NUM_TEAMS)]
    pool_actual = player_pool.copy()
    accuracy_stats = {'top1': 0, 'top3': 0, 'top5': 0, 'top10': 0, 'top15': 0, 'total': 0}

    for rnd, round_picks in enumerate(draft_rounds):
        for idx, original_player_name in enumerate(round_picks):
            team = teams_actual[idx]
            available_choices = [p for p in pool_actual if team.can_add_player(p)]

            # Get top N recommendations for accuracy check
            top1 = get_top_n_recommendations(team, available_choices, n=1)
            top3 = get_top_n_recommendations(team, available_choices, n=3)
            top5 = get_top_n_recommendations(team, available_choices, n=5)
            top10 = get_top_n_recommendations(team, available_choices, n=10)
            top15 = get_top_n_recommendations(team, available_choices, n=15)
            accuracy_stats['total'] += 1
            actual_pick = find_player_by_name(original_player_name, available_choices)
            if actual_pick:
                # Find the index (0-based) of the actual pick in the recommendations
                idx_in_recs = next((i for i, p in enumerate(top15) if p['Player'] == actual_pick['Player']), None)
                if idx_in_recs is not None:
                    if idx_in_recs == 0:
                        accuracy_stats['top1'] += 1
                    elif idx_in_recs < 3:
                        accuracy_stats['top3'] += 1  # 2nd or 3rd best
                    elif idx_in_recs < 5:
                        accuracy_stats['top5'] += 1  # 4th or 5th best
                    elif idx_in_recs < 10:
                        accuracy_stats['top10'] += 1 # 6th-10th best
                    elif idx_in_recs < 15:
                        accuracy_stats['top15'] += 1 # 11th-15th best
                team.add_player(actual_pick)
                pool_actual.remove(actual_pick)
            else:
                # If the player is not available, skip (should not happen if CSV and pool match)
                pass

    # --- Simulate Recommended Draft ---
    teams_recommended = [Team(f"Team {i+1}", roster_requirements) for i in range(NUM_TEAMS)]
    pool_recommended = player_pool.copy()
    recommended_picks = []

    for rnd in range(ROUNDS):
        for idx in range(NUM_TEAMS):
            team = teams_recommended[idx]
            available_choices = [p for p in pool_recommended if team.can_add_player(p)]
            rec = recommend_pick(team, available_choices)
            if rec:
                team.add_player(rec)
                pool_recommended.remove(rec)
                recommended_picks.append(rec['Player'])
            else:
                recommended_picks.append(None)
    print("\n=== Recommended Draft (every team takes top recommendation) ===")
    for rnd in range(ROUNDS):
        print(f"Round {rnd+1}:")
        for idx in range(NUM_TEAMS):
            pick_num = rnd * NUM_TEAMS + idx
            print(f"  Team {idx+1}: {recommended_picks[pick_num]}")
        print()
    # --- Report accuracy statistics ---
    print("\n=== Draft Accuracy Stats (Actual Draft vs Recommendations) ===")
    print(f"Total picks: {accuracy_stats['total']}")
    print(f"Exact recommended pick taken: {accuracy_stats['top1']} ({accuracy_stats['top1']/accuracy_stats['total']*100:.1f}%)")
    print(f"Pick was 2nd or 3rd best: {accuracy_stats['top3']} ({accuracy_stats['top3']/accuracy_stats['total']*100:.1f}%)")
    print(f"Pick was 4th or 5th best: {accuracy_stats['top5']} ({accuracy_stats['top5']/accuracy_stats['total']*100:.1f}%)")
    print(f"Pick was 6th-10th best: {accuracy_stats['top10']} ({accuracy_stats['top10']/accuracy_stats['total']*100:.1f}%)")
    print(f"Pick was 11th-15th best: {accuracy_stats['top15']} ({accuracy_stats['top15']/accuracy_stats['total']*100:.1f}%)")

    # --- Additional statistics ---
    # 1. Average recommendation rank
    rec_ranks = []
    for rnd, round_picks in enumerate(draft_rounds):
        for idx, original_player_name in enumerate(round_picks):
            team = teams_actual[idx]
            available_choices = [p for p in pool_actual if team.can_add_player(p)]
            top15 = get_top_n_recommendations(team, available_choices, n=15)
            actual_pick = find_player_by_name(original_player_name, available_choices)
            if actual_pick:
                idx_in_recs = next((i for i, p in enumerate(top15) if p['Player'] == actual_pick['Player']), None)
                if idx_in_recs is not None:
                    rec_ranks.append(idx_in_recs + 1)  # 1-based rank

    avg_rank = sum(rec_ranks) / len(rec_ranks) if rec_ranks else 0
    print(f"\nAverage recommendation rank for actual picks: {avg_rank:.2f}")

    # 2. Team-by-team accuracy
    team_accuracy = [0] * NUM_TEAMS
    for idx in range(NUM_TEAMS):
        matches = 0
        for rnd in range(ROUNDS):
            team = teams_actual[idx]
            available_choices = [p for p in pool_actual if team.can_add_player(p)]
            top1 = get_top_n_recommendations(team, available_choices, n=1)
            actual_pick_name = draft_rounds[rnd][idx]
            if top1 and top1[0]['Player'] == actual_pick_name:
                matches += 1
        team_accuracy[idx] = matches
    print("\nTeam-by-team exact recommendation matches:")
    for idx, matches in enumerate(team_accuracy):
        print(f"  Team {idx+1}: {matches} / {ROUNDS}")

    # 3. Position accuracy
    pos_accuracy = {}
    for rnd, round_picks in enumerate(draft_rounds):
        for idx, original_player_name in enumerate(round_picks):
            team = teams_actual[idx]
            available_choices = [p for p in pool_actual if team.can_add_player(p)]
            top1 = get_top_n_recommendations(team, available_choices, n=1)
            actual_pick = find_player_by_name(original_player_name, available_choices)
            if actual_pick and top1:
                actual_pos = ''.join([c for c in actual_pick['POS'] if not c.isdigit()])
                rec_pos = ''.join([c for c in top1[0]['POS'] if not c.isdigit()])
                if actual_pos not in pos_accuracy:
                    pos_accuracy[actual_pos] = {'matches': 0, 'total': 0}
                pos_accuracy[actual_pos]['total'] += 1
                if actual_pos == rec_pos:
                    pos_accuracy[actual_pos]['matches'] += 1
    print("\nPosition accuracy (actual pick matches recommended position):")
    for pos, stats in pos_accuracy.items():
        pct = stats['matches'] / stats['total'] * 100 if stats['total'] else 0
        print(f"  {pos}: {stats['matches']} / {stats['total']} ({pct:.1f}%)")

    # 4. Missed picks (not in top 15)
    missed_picks = 0
    for rnd, round_picks in enumerate(draft_rounds):
        for idx, original_player_name in enumerate(round_picks):
            team = teams_actual[idx]
            available_choices = [p for p in pool_actual if team.can_add_player(p)]
            top15 = get_top_n_recommendations(team, available_choices, n=15)
            actual_pick = find_player_by_name(original_player_name, available_choices)
            if actual_pick:
                idx_in_recs = next((i for i, p in enumerate(top15) if p['Player'] == actual_pick['Player']), None)
                if idx_in_recs is None:
                    missed_picks += 1
    print(f"\nMissed picks (actual pick not in top 15 recommendations): {missed_picks}")

    # 5. Roster value comparison (sum projected points for each team)
    def get_team_points(team):
        return sum(p.get('Proj', 0) for p in team.roster)

    print("\nRoster value comparison (actual vs recommended, sum of projected points):")
    for idx in range(NUM_TEAMS):
        actual_points = get_team_points(teams_actual[idx])
        recommended_points = get_team_points(teams_recommended[idx])
        print(f"  Team {idx+1}: Actual {actual_points:.1f}, Recommended {recommended_points:.1f}")

    # 6. Draft deviation (number of times each team deviated from top recommendation)
    team_deviation = [0] * NUM_TEAMS
    for rnd, round_picks in enumerate(draft_rounds):
        for idx, original_player_name in enumerate(round_picks):
            team = teams_actual[idx]
            available_choices = [p for p in pool_actual if team.can_add_player(p)]
            top1 = get_top_n_recommendations(team, available_choices, n=1)
            actual_pick = find_player_by_name(original_player_name, available_choices)
            if actual_pick and top1 and actual_pick['Player'] != top1[0]['Player']:
                team_deviation[idx] += 1
    print("\nDraft deviation (times each team did NOT take top recommendation):")
    for idx, dev in enumerate(team_deviation):
        print(f"  Team {idx+1}: {dev} / {ROUNDS}")

    # After the draft simulation, reload player pool for stats:
    stats_pool = load_player_pool().to_dict('records')
    stats_teams = [Team(f"Team {i+1}", roster_requirements) for i in range(NUM_TEAMS)]

    # Re-run the actual draft for stats, but do NOT remove players from stats_pool
    for rnd, round_picks in enumerate(draft_rounds):
        for idx, original_player_name in enumerate(round_picks):
            team = stats_teams[idx]
            available_choices = [p for p in stats_pool if team.can_add_player(p)]
            actual_pick = find_player_by_name(original_player_name, available_choices)
            if actual_pick:
                team.add_player(actual_pick)
                # Do NOT remove from stats_pool

    # Now use stats_teams and stats_pool for all statistics

if __name__ == "__main__":
    main()
import random
import os
import pandas as pd
from player_pool import load_player_pool

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
        # FLEX logic: allow RB/WR/TE if FLEX is needed
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
        # Update counts
        if self.counts.get(pos) is not None:
            self.counts[pos] += 1
        elif pos in ['RB', 'WR', 'TE'] and self.counts.get('FLEX') is not None and self.counts['FLEX'] < self.requirements['FLEX']:
            self.counts['FLEX'] += 1
        else:
            self.counts['BENCH'] += 1

def cpu_pick(team, player_pool, recent_picks, round_num=1):
    needs = team.needs()
    scores = []

    # Count recent picks by position for run awareness
    run_counts = {}
    for pos, _ in recent_picks:
        base_pos = ''.join([c for c in pos if not c.isdigit()])
        run_counts[base_pos] = run_counts.get(base_pos, 0) + 1

    rb_count = sum(1 for p in team.roster if 'RB' in p['POS'])
    wr_count = sum(1 for p in team.roster if 'WR' in p['POS'])

    for i, player in enumerate(player_pool[:30]):
        pos = ''.join([c for c in player['POS'] if not c.isdigit()])
        score = 0

        # --- Early round logic ---
        if round_num <= 2:
            # Discourage more than 1 RB in first 2 rounds
            if pos == 'RB' and rb_count >= 1:
                score -= 100
            # Encourage WRs in first 2 rounds
            if pos == 'WR':
                score += 10
            # Slightly encourage elite QB/TE in first 2 rounds
            if pos in ['QB', 'TE'] and i < 5:
                score += 3
            # NO team need bonus in first 2 rounds!
        else:
            # Team need: very small boost after round 2
            if needs.get(pos, 0) > 0 or (pos in ['RB', 'WR', 'TE'] and needs.get('FLEX', 0) > 0):
                score += 4

        # ADP/VORP value (main driver)
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
                score += 2

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

def recommend_pick(team, player_pool):
    needs = team.needs()
    # Prioritize filling needs, then best available
    for player in player_pool:
        pos = ''.join([c for c in player['POS'] if not c.isdigit()])
        if team.can_add_player(player):
            # Recommend first player that fills a need (including FLEX)
            if needs.get(pos, 0) > 0 or (pos in ['RB', 'WR', 'TE'] and needs.get('FLEX', 0) > 0):
                return player
    # If all needs are filled, recommend best available
    for player in player_pool:
        if team.can_add_player(player):
            return player
    return None

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
    player_pool = load_player_pool().to_dict('records')
    teams = [Team(f"Team {i+1}", roster_requirements) for i in range(NUM_TEAMS)]

    # Choose draft position
    user_team_idx = int(input("Enter your draft position (1-12): ")) - 1
    print(f"You're drafting at position {user_team_idx + 1}")

    # Choose draft mode
    print("\nDraft mode options:")
    print("1. Enter picks manually for each team")
    print("2. Provide a CSV file with draft order")
    print("3. Simulate entire draft (each team takes top recommendation)")
    mode = input("Choose draft mode (1/2/3): ").strip()

    if mode == "1":
        print("\nManual entry mode. Enter player names for each pick.")
        for rnd in range(ROUNDS):
            print(f"\n--- Round {rnd+1} ---")
            for pick in range(NUM_TEAMS):
                # Snake order logic
                if rnd % 2 == 0:
                    team_idx = pick
                else:
                    team_idx = NUM_TEAMS - 1 - pick
                team = teams[team_idx]
                available_choices = [p for p in player_pool if team.can_add_player(p)]
                if team_idx == user_team_idx:
                    available_choices = [
                        p for p in available_choices
                        if p['Player'].strip().lower() not in ['rashee rice', 'terry mclaurin']
                    ]
                print(f"Team {team_idx+1} ({team.name}) pick:")
                print("Available players:")
                for i, p in enumerate(available_choices[:10]):
                    print(f"{i+1}. {p['Player']} ({p['POS']})")
                player_name = input("Enter player name: ").strip()
                chosen = find_player_by_name(player_name, available_choices)
                if chosen:
                    team.add_player(chosen)
                    player_pool.remove(chosen)
                    print(f"Team {team_idx+1} drafted {chosen['Player']} ({chosen['POS']})")
                else:
                    print("Player not found or not eligible. Skipping pick.")

    elif mode == "2":
        draft_order_path = input("Enter path to draft order CSV: ").strip()
        draft_df = pd.read_csv(draft_order_path, delimiter='\t')
        draft_picks = draft_df['Player'].tolist()  # Flat list in pick order

        total_picks = NUM_TEAMS * ROUNDS
        assert len(draft_picks) >= total_picks, "Not enough picks in draft file!"

        deferred_picks = {}  # position -> list of deferred players

        for pick_num, original_player_name in enumerate(draft_picks[:total_picks]):
            round_num = pick_num // NUM_TEAMS
            # Determine team index for this pick (snake order)
            if round_num % 2 == 0:
                team_idx = pick_num % NUM_TEAMS
            else:
                team_idx = NUM_TEAMS - 1 - (pick_num % NUM_TEAMS)
            team = teams[team_idx]
            available_choices = [p for p in player_pool if team.can_add_player(p)]

            # For your team, filter out Rashee Rice and Terry McLaurin
            if team_idx == user_team_idx:
                available_choices = [
                    p for p in available_choices
                    if p['Player'].strip().lower() not in ['rashee rice', 'terry mclaurin']
                ]

            recommended = recommend_pick(team, available_choices if team_idx == user_team_idx else player_pool)

            if team_idx == user_team_idx:
                # Always pick recommended
                if recommended:
                    team.add_player(recommended)
                    player_pool.remove(recommended)
                    print(f"Team {team_idx+1} (You) drafted {recommended['Player']} ({recommended['POS']})")
                    # If original pick != recommended, defer original pick
                    if normalize(original_player_name) != normalize(recommended['Player']):
                        orig_player = find_player_by_name(original_player_name, available_choices)
                        if orig_player:
                            pos = ''.join([c for c in orig_player['POS'] if not c.isdigit()])
                            deferred_picks.setdefault(pos, []).append(orig_player)
            else:
                orig_player = find_player_by_name(original_player_name, available_choices)
                pos = ''.join([c for c in orig_player['POS'] if not c.isdigit()]) if orig_player else None
                deferred_pool = deferred_picks.get(pos, [])
                candidates = []

                # Only include original pick if available
                if orig_player and orig_player in player_pool:
                    candidates.append(orig_player)
                # Only include deferred players if available
                deferred_available = [p for p in deferred_pool if p in player_pool]
                candidates.extend(deferred_available)

                if candidates:
                    chosen = random.choice(candidates)
                    team.add_player(chosen)
                    if chosen in player_pool:
                        player_pool.remove(chosen)
                    if chosen in deferred_pool:
                        deferred_pool.remove(chosen)
                    print(f"Team {team_idx+1} drafted {chosen['Player']} ({chosen['POS']}) [random from deferred/original]")
                else:
                    # Fallback: take recommended
                    recommended_other = recommend_pick(team, available_choices)
                    if recommended_other:
                        team.add_player(recommended_other)
                        player_pool.remove(recommended_other)
                        print(f"Team {team_idx+1} drafted recommended {recommended_other['Player']} ({recommended_other['POS']})")
                    else:
                        print(f"Team {team_idx+1} could not draft anyone!")

    elif mode == "3":
        print("\nSimulating entire draft: each team takes top recommendation.")
        for rnd in range(ROUNDS):
            for pick in range(NUM_TEAMS):
                # Snake order logic
                if rnd % 2 == 0:
                    team_idx = pick
                else:
                    team_idx = NUM_TEAMS - 1 - pick
                team = teams[team_idx]
                available_choices = [p for p in player_pool if team.can_add_player(p)]
                if team_idx == user_team_idx:
                    available_choices = [
                        p for p in available_choices
                        if p['Player'].strip().lower() not in ['rashee rice', 'terry mclaurin']
                    ]
                recommended = recommend_pick(team, available_choices)
                if recommended:
                    team.add_player(recommended)
                    player_pool.remove(recommended)
                    print(f"Team {team_idx+1} drafted {recommended['Player']} ({recommended['POS']})")
                else:
                    print(f"Team {team_idx+1} could not draft anyone!")

    else:
        print("Invalid mode selected.")

    print("\nDraft complete! Your team:")
    for p in teams[user_team_idx].roster:
        print(f"{p['Player']} ({p['POS']})")

    print("\n=== Full Draft Results ===")
    for i, team in enumerate(teams):
        print(f"\n{team.name}'s roster:")
        for p in team.roster:
            print(f"  {p['Player']} ({p['POS']})")

if __name__ == "__main__":
    main()
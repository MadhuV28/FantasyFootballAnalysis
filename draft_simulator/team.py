class Team:
    def __init__(self, name, roster_requirements):
        self.name = name
        self.roster = []
        self.roster_requirements = roster_requirements.copy()
        self.filled = {pos: 0 for pos in roster_requirements}

    def add_player(self, player):
        pos = ''.join([c for c in player['POS'] if not c.isdigit()])  # e.g., WR3 -> WR
        self.roster.append(player)
        if pos in self.filled:
            self.filled[pos] += 1

    def needs(self):
        return {pos: self.roster_requirements[pos] - self.filled[pos] for pos in self.roster_requirements}

    def can_add_player(self, player):
        pos = ''.join([c for c in player['POS'] if not c.isdigit()])
        current_count = sum(1 for p in self.roster if pos in p['POS'])
        starters_needed = self.roster_requirements.get(pos, 0)
        bench_needed = self.roster_requirements.get('BENCH', 0)
        if current_count < starters_needed:
            return True
        bench_count = len(self.roster) - sum(self.roster_requirements.values()) + bench_needed
        return bench_count < bench_needed
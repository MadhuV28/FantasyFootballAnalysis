import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from draft_simulator.player_pool import load_player_pool

def test_load_player_pool():
    df = load_player_pool()
    assert not df.empty
    assert "Player" in df.columns

from draft_simulator.team import Team

def test_team_needs():
    reqs = {"QB": 1, "RB": 2}
    team = Team("Test", reqs)
    assert team.needs() == {"QB": 1, "RB": 2}
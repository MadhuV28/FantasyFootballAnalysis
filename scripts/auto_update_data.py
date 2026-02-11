import os
import time
import requests
import pandas as pd

# ----------------------------
# Config
# ----------------------------
DATA_OUT_REL = "../DataInfo/2025proj/latest_projections.csv"  # relative to this script's directory
TIMEOUT_SEC = 30

PLAYERS_URL = "https://api.sleeper.app/v1/players/nfl"
STATE_URL = "https://api.sleeper.app/v1/state/nfl"  # used to auto-detect season/week
PROJECTIONS_URL_TEMPLATE = "https://api.sleeper.app/projections/nfl/{season}/{week}"

# Positions you care about (you can remove K/DEF if you want)
POSITIONS = ["QB", "RB", "WR", "TE", "K", "DEF"]

# regular | postseason (regular is typical)
SEASON_TYPE = "regular"

# Flatten the nested "stats" dict into columns in the output CSV
FLATTEN_STATS = True

# Be polite to the API
SLEEP_BETWEEN_CALLS_SEC = 0.5


# ----------------------------
# Helpers
# ----------------------------
def script_dir() -> str:
    return os.path.dirname(os.path.abspath(__file__))


def output_path() -> str:
    # Resolve output path relative to the script directory, not the current working directory
    return os.path.abspath(os.path.join(script_dir(), DATA_OUT_REL))


def get_current_season_week() -> tuple[int, int]:
    """
    Uses Sleeper's NFL state endpoint to determine the current season and week.
    If you prefer hardcoding, you can skip this and just set season/week manually.
    """
    r = requests.get(STATE_URL, timeout=TIMEOUT_SEC)
    r.raise_for_status()
    s = r.json()
    season = int(s.get("season"))
    week = int(s.get("week"))
    return season, week


def fetch_players() -> pd.DataFrame:
    """
    Fetch player metadata. Sleeper returns a dict keyed by player_id.
    We convert it into a DataFrame with a single, unique 'player_id' column.
    """
    r = requests.get(PLAYERS_URL, timeout=TIMEOUT_SEC)
    r.raise_for_status()
    players = r.json()  # dict keyed by player_id

    # Build DF from dict; index becomes player_id
    players_df = pd.DataFrame.from_dict(players, orient="index").reset_index()
    players_df = players_df.rename(columns={"index": "player_id"})

    # Ensure no duplicate column labels (sometimes inner payload includes player_id too)
    players_df = players_df.loc[:, ~players_df.columns.duplicated()]

    # Keep only useful columns (add more if you want)
    keep = ["player_id", "full_name", "position", "team", "age", "status"]
    keep = [c for c in keep if c in players_df.columns]
    players_df = players_df[keep].drop_duplicates(subset=["player_id"])

    return players_df


def fetch_weekly_projections(season: int, week: int) -> pd.DataFrame:
    """
    Fetch weekly projections for given season/week.
    IMPORTANT: include season_type + position[] params (otherwise 400 Bad Request is common).
    """
    url = PROJECTIONS_URL_TEMPLATE.format(season=season, week=week)
    params = {
        "season_type": SEASON_TYPE,
        "position[]": POSITIONS,
    }

    r = requests.get(url, params=params, timeout=TIMEOUT_SEC)
    # Helpful debug if it fails
    if not r.ok:
        raise requests.HTTPError(
            f"{r.status_code} {r.reason} for url: {r.url}\nResponse: {r.text[:500]}"
        )

    projections = r.json()  # list[dict]
    proj_df = pd.DataFrame(projections)

    # Ensure expected key exists
    if "player_id" not in proj_df.columns:
        raise ValueError(
            f"Unexpected projections response shape. Columns: {proj_df.columns.tolist()}"
        )

    return proj_df


def build_projection_table(season: int, week: int) -> pd.DataFrame:
    print(f"[INFO] Fetching Sleeper players metadata...")
    players_df = fetch_players()
    print(f"[INFO] Players rows: {len(players_df):,}")

    time.sleep(SLEEP_BETWEEN_CALLS_SEC)

    print(f"[INFO] Fetching Sleeper projections for season={season}, week={week}, season_type={SEASON_TYPE}...")
    proj_df = fetch_weekly_projections(season, week)
    print(f"[INFO] Projections rows: {len(proj_df):,}")

    # Merge projections with player metadata
    df = proj_df.merge(players_df, on="player_id", how="left")

    # Optional: flatten nested stats dict into columns
    if FLATTEN_STATS and "stats" in df.columns:
        stats_flat = pd.json_normalize(df["stats"])
        stats_flat.columns = [f"stat_{c}" for c in stats_flat.columns]
        df = pd.concat([df.drop(columns=["stats"]), stats_flat], axis=1)

    # Nice-to-have: move common columns to the front if they exist
    front = [c for c in ["player_id", "full_name", "team", "position", "points"] if c in df.columns]
    rest = [c for c in df.columns if c not in front]
    df = df[front + rest]

    return df


def save_projections(df: pd.DataFrame, out_path: str) -> None:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f"[OK] Saved {len(df):,} rows to: {out_path}")


# ----------------------------
# Main
# ----------------------------
if __name__ == "__main__":
    try:
        print(f"[INFO] Running: {__file__}")
        print(f"[INFO] CWD: {os.getcwd()}")

        # Auto-detect current season/week (recommended)
        season, week = get_current_season_week()

        df = build_projection_table(season, week)
        save_projections(df, output_path())

        print("[DONE] Update complete.")
    except Exception as e:
        print(f"[ERROR] Error updating projections: {e}")
        raise

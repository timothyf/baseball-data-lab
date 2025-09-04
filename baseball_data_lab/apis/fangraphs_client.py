from baseball_data_lab.config.paths import FANGRAPHS_BASE_URL, FANGRAPHS_NEXT_URL
import pandas as pd
import requests




class FangraphsClient:

    # Example URL for fetching pitching stats for a specific player in a specific season:
    # https://www.fangraphs.com/api/leaders/major-league/data
    # Query Parameters:
    # - pos=all: Position filter (all positions)
    # - stats=pit: Stats type (pitching)
    # - lg=all: League filter (all leagues)
    # - qual=0: Qualification filter (no minimum qualifications)
    # - season=2025: Season year
    # - startdate=2025-03-01: Start date of the season
    # - enddate=2025-11-01: End date of the season
    # - month=33: Month filter (entire season) 
    # - players=22267: Player Fangraphs ID

    # Past Seasons
    # set month=0
    # with 1 team
    # https://www.fangraphs.com/api/leaders/major-league/data?pos=all&stats=pit&lg=all&qual=0&season=2024&startdate=2024-03-01&enddate=2024-11-01&month=0&players=22267

    # with 2 teams
    # https://www.fangraphs.com/api/leaders/major-league/data?pos=all&stats=pit&lg=all&qual=0&season=2024&startdate=2024-03-01&enddate=2024-11-01&month=0&players=17479


    # Current Season
    # set month=33
    # https://www.fangraphs.com/api/leaders/major-league/data?pos=all&stats=pit&lg=all&qual=0&season=2025&startdate=2025-03-01&enddate=2025-11-01&month=33&players=22267
    @staticmethod
    def fetch_player_stats(player_fangraphs_id: int, season: int, fangraphs_team_id: int, stat_type: str):
        month = 0 if season < 2025 else 33
        if stat_type == 'pitching':
            stat = 'pit'
        elif stat_type == 'batting':
            stat = 'bat'
        else:
            raise ValueError("Invalid stat_type. Must be 'pitching' or 'batting'")

        start_date = f"{season}-03-01"
        end_date = f"{season}-11-01"

        if fangraphs_team_id is not None:
            url = (
                f"{FANGRAPHS_BASE_URL}?pos=all&stats={stat}&lg=all&qual=0"
                f"&season={season}&startdate={start_date}&enddate={end_date}"
                f"&month={month}&team={fangraphs_team_id}&players={player_fangraphs_id}"
            )
        else:
            url = (
                f"{FANGRAPHS_BASE_URL}?pos=all&stats={stat}&lg=all&qual=0"
                f"&season={season}&startdate={start_date}&enddate={end_date}"
                f"&month={month}&players={player_fangraphs_id}"
            )
        data = requests.get(url).json()
        df = pd.DataFrame(data=data['data'])
        return df

    @staticmethod
    def _fetch_leaderboards(season: int, stat: str, as_json: bool = False):
        """Build the Fangraphs leaderboard URL and return data.

        Parameters
        ----------
        season: int
            Season to query.
        stat: str
            Statistic type used by Fangraphs (e.g. ``"bat"`` or ``"pit"``).
        as_json: bool, default False
            If True return the raw JSON payload, otherwise return a DataFrame.
        """
        url = (
            f"{FANGRAPHS_BASE_URL}?age=&pos=all&stats={stat}&lg=all"
            f"&season={season}&season1={season}&ind=0&qual=0&type=8"
            f"&month=0&pageitems=500000"
        )
        data = requests.get(url).json()
        if as_json:
            return data
        return pd.DataFrame(data=data["data"])

    @staticmethod
    def fetch_leaderboards(season: int, stat_type: str, as_json: bool = False):
        stat_map = {"pitching": "pit", "batting": "bat"}
        try:
            stat = stat_map[stat_type]
        except KeyError:
            raise ValueError("Invalid stat_type. Must be 'pitching' or 'batting'")
        return FangraphsClient._fetch_leaderboards(season, stat, as_json=as_json)

    @staticmethod
    def fetch_pitching_leaderboards(season: int):
        return FangraphsClient._fetch_leaderboards(season, "pit")
    
    # Sample
    # https://www.fangraphs.com/api/leaders/major-league/data?age=&pos=all&stats=bat&lg=all&season=2024&season1=2024&ind=0&qual=0&type=8&month=0&pageitems=10
    @staticmethod
    def fetch_batting_leaderboards(season: int):
        return FangraphsClient._fetch_leaderboards(season, "bat")
    
    @staticmethod
    def fetch_batting_leaderboards_as_json(season: int):
        return FangraphsClient._fetch_leaderboards(season, "bat", as_json=True)
    
    @staticmethod
    def fetch_pitching_leaderboards_as_json(season: int):
        return FangraphsClient._fetch_leaderboards(season, "pit", as_json=True)
    

    # FANGRAPHS_BASE_URL = "https://www.fangraphs.com/api/leaders/major-league/data"
    # https://www.fangraphs.com/api/leaders/major-league/data?age=&pos=all&stats=bat&lg=all&qual=0&season=2024&season1=2024&startdate=2024-03-01&enddate=2024-11-01&month=0&hand=&team=13&pageitems=30&pagenum=1&ind=0&rost=0&players=0&type=8&postseason=&sortdir=default&sortstat=WAR
    # https://www.fangraphs.com/api/leaders/major-league/data?age=&pos=all&stats=bat&lg=all&qual=0&season=2021&season1=2021&hand=&team=6&pageitems=30&pagenum=1&ind=0&rost=0&players=0&type=8&postseason=&sortdir=default&sortstat=WAR
    @staticmethod
    def fetch_team_players(team_id: int, season: int):

        # Fetch all batting stats for the team in the given year
        #url = f"{FANGRAPHS_BASE_URL}?age=&pos=all&stats=bat&lg=all&qual=0&season=2024&season1={season}&startdate=2024-03-01&enddate=2024-11-01&month=0&hand=&team={team_id}&pageitems=30&pagenum=1&ind=0&rost=0&players=0&type=8&postseason=&sortdir=default&sortstat=WAR"
        url = (
            f"{FANGRAPHS_BASE_URL}?age=&pos=all&stats=bat&lg=all&qual=0"
            f"&season={season}&season1={season}&hand=&team={team_id}"
            f"&pageitems=800&pagenum=1&ind=0&rost=0&players=0&type=8"
            f"&postseason=&sortdir=default&sortstat=WAR"
        )

        batting_stats = requests.get(url).json()['data']
        #print(f"batting_stats = {batting_stats}")

        # Fetch all pitching stats for the team in the given year
        url = f"{FANGRAPHS_BASE_URL}?age=&pos=all&stats=pit&lg=all&qual=0&season={season}&season1={season}&hand=&team={team_id}&pageitems=800&pagenum=1&ind=0&rost=0&players=0&type=8&postseason=&sortdir=default&sortstat=WAR"
        pitching_stats = requests.get(url).json()['data']

        # Combine player names from both batting and pitching stats
        # batters = set(batting_stats['Name'])
        # pitchers = set(pitching_stats['Name'])

        # Extract names from the data
        # batters = [extract_name(entry['Name']) for entry in batting_stats]
        # pitchers = [extract_name(entry['Name']) for entry in pitching_stats]

        batters = [(entry['PlayerName']) for entry in batting_stats]
        pitchers = [(entry['PlayerName']) for entry in pitching_stats]
        
        # Merge both sets to get all unique players
        all_players = list(set(batters) | set(pitchers))

        return sorted(all_players)

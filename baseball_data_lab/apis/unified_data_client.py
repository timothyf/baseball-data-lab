import pandas as pd
from typing import List, Optional
import logging

from baseball_data_lab.apis.web_client import WebClient
from baseball_data_lab.apis.mlb_stats_client import MlbStatsClient
from baseball_data_lab.apis.pybaseball_client import PybaseballClient
from baseball_data_lab.apis.fangraphs_client import FangraphsClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from baseball_data_lab.apis.chadwick_register import (
    ChadwickRegister,
    PlayerSearchClient,
)
from baseball_data_lab.utils import Utils


class UnifiedDataClient:

    def __init__(self):
        register = ChadwickRegister()
        register.load(save=False)
        self.search_client = PlayerSearchClient(register)

    #############################
    # FangraphsClient wrappers
    #############################

    def _fetch_player_stats(
        self,
        mlbam_id: int,
        season: int,
        stat_type: str,
        fangraphs_team_id: Optional[int] = None,
    ) -> pd.DataFrame:
        """Internal helper to fetch Fangraphs stats for a player."""
        player_fangraphs_id = Utils.get_fangraphs_id(
            mlbam_id=mlbam_id, search_client=self.search_client
        )
        if player_fangraphs_id == -1:
            if mlbam_id == 690916:
                player_fangraphs_id = 30160
            elif mlbam_id == 695578:
                player_fangraphs_id = 29518
            elif mlbam_id == 702616:
                player_fangraphs_id = 31781
            else:
                raise ValueError(f"Invalid Fangraphs ID for player {mlbam_id}.")

        return FangraphsClient.fetch_player_stats(
            player_fangraphs_id=player_fangraphs_id,
            season=season,
            fangraphs_team_id=fangraphs_team_id,
            stat_type=stat_type,
        )

    def fetch_player_stats(
        self,
        mlbam_id: int,
        season: int,
        stat_type: str,
        fangraphs_team_id: Optional[int] = None,
    ) -> pd.DataFrame:
        """Fetch batting or pitching stats for a player."""
        return self._fetch_player_stats(
            mlbam_id=mlbam_id,
            season=season,
            stat_type=stat_type,
            fangraphs_team_id=fangraphs_team_id,
        )

    def _fetch_leaderboards(
        self, season: int, stat_type: str, as_json: bool = False
    ):
        """Internal helper to fetch Fangraphs leaderboards."""
        if as_json:
            if stat_type == "pitching":
                return FangraphsClient.fetch_pitching_leaderboards_as_json(season)
            if stat_type == "batting":
                return FangraphsClient.fetch_batting_leaderboards_as_json(season)
            raise ValueError("Invalid stat_type. Must be 'pitching' or 'batting'")
        return FangraphsClient.fetch_leaderboards(season, stat_type)

    def fetch_leaderboards(
        self, season: int, stat_type: str, as_json: bool = False
    ):
        """Fetch batting or pitching leaderboards."""
        return self._fetch_leaderboards(season, stat_type, as_json=as_json)

    def fetch_team_players(self, team_id: int, season: int):
        return FangraphsClient.fetch_team_players(team_id, season)

    def fetch_batting_leaderboards(self, season: int, as_json: bool = False):
        return self.fetch_leaderboards(season, "batting", as_json=as_json)

    def fetch_pitching_leaderboards(self, season: int, as_json: bool = False):
        return self.fetch_leaderboards(season, "pitching", as_json=as_json)

    #############################
    # MlbStatsClient wrappers
    #############################
    def fetch_batting_splits(self, player_id: int, season: int, sit_codes: Optional[List[str]] = None):
        return MlbStatsClient.fetch_batter_stat_splits(player_id, season, sit_codes=sit_codes)

    def fetch_pitching_splits(self, player_id: int, season: int, sit_codes: Optional[List[str]] = None):
        return MlbStatsClient.fetch_pitcher_stat_splits(player_id, season, sit_codes=sit_codes)

    def fetch_active_roster(
        self, team_id: int = None,  year: int = 2024
    ):
        return MlbStatsClient.fetch_active_roster(team_id, year)

    def fetch_team(self, team_id: int):
        return MlbStatsClient.fetch_team(team_id)

    def fetch_full_season_roster(self, team_id: int, year: int = 2024):
        return MlbStatsClient.fetch_full_season_roster(team_id, year)

    def fetch_season_info(self, year: int):
        return MlbStatsClient.fetch_season_info(year)

    def fetch_team_id(self, team_name: str):
        return MlbStatsClient.fetch_team_id(team_name)

    def fetch_player_info(self, player_id: int):
        return MlbStatsClient.fetch_player_info(player_id)

    # def fetch_player_stats(self, player_id: int, year: int):
    #     return MlbStatsClient.fetch_player_stats(player_id, year)

    def fetch_player_stats_by_season(self, player_id: int, year: int):
        return MlbStatsClient.fetch_player_stats_by_season(player_id, year)

    def fetch_player_team_stats(self, player_id: int, year: int):
        return MlbStatsClient.fetch_player_team_stats(player_id, year)

    def fetch_player_teams_for_season(
        self, player_id: int, year: int, group: str = None, ids_only: bool = False
    ):
        return MlbStatsClient.fetch_player_teams_for_season(
            player_id, year, group=group, ids_only=ids_only
        )

    def fetch_player_gamelog(self, player_id: int, stat_type: str, season: int):
        return MlbStatsClient.fetch_player_gamelog(player_id, stat_type, season)

    def fetch_player_team(self, player_id: int, year: int):
        return MlbStatsClient.fetch_player_team(player_id, year)

    def fetch_player_mlbam_id(self, player_id: int):
        return MlbStatsClient.fetch_player_mlbam_id(player_id)

    def fetch_standings_data(self, season: int, league_ids: str) -> pd.DataFrame:
        return MlbStatsClient.fetch_standings_data(season, league_ids)

    def fetch_team_record_for_season(self, season: int, team_id: int) -> pd.DataFrame:
        return MlbStatsClient.fetch_team_record_for_season(season, team_id)

    def fetch_schedule_for_date_range(
        self, start_date: str, end_date: str
    ) -> pd.DataFrame:
        return MlbStatsClient.fetch_schedule_for_date_range(start_date, end_date)

    def fetch_team_logo_url(self, mlbam_team_id: int) -> str:
        return MlbStatsClient.fetch_team_logo_url(mlbam_team_id)

    def fetch_team_spot_url(self, mlbam_team_id: int, size: int) -> str:
        return MlbStatsClient.fetch_team_spot_url(mlbam_team_id, size)
    
    def fetch_player_hero_image_url(self, player_id: int) -> str:
        return MlbStatsClient.fetch_player_hero_image_url(player_id)

    def fetch_game_data(self, game_pk: int) -> pd.DataFrame:
        return MlbStatsClient.fetch_game_data(game_pk)

    def fetch_game_live_feed(self, game_pk: int) -> pd.DataFrame:
        return MlbStatsClient.fetch_game_live_feed(game_pk)

    def fetch_recent_schedule_for_team(self, team_id: int) -> pd.DataFrame:
        return MlbStatsClient.fetch_recent_schedule_for_team(team_id)

    def fetch_game_boxscore_data(game_pk: int) -> pd.DataFrame:
        return MlbStatsClient.fetch_game_boxscore_data(game_pk)

    def fetch_active_players(self, season: int) -> pd.DataFrame:
        return MlbStatsClient.fetch_active_players(season)

    def fetch_player_stats_career(self, player_id: int):
        return MlbStatsClient.fetch_player_stats_career(player_id)
    
    def fetch_career_stats_for_players(self, player_ids: list[int]):
        return MlbStatsClient.fetch_career_stats_for_players(player_ids)

    def fetch_leaderboard_data(
        self,
        season: int,
        league_ids: str,
        team_id: str,
        group: str,
        stat_type: str,
        limit: int,
        offset: int,
        sort_order: str,
    ) -> pd.DataFrame:
        return MlbStatsClient.fetch_leaderboard_data(
            season, league_ids, team_id, group, stat_type, limit, offset, sort_order
        )

    def fetch_situation_codes(self):
        return MlbStatsClient.fetch_situation_codes()

    #############################
    # PybaseballClient wrappers
    #############################
    def fetch_batting_splits_leaderboards(
        self, player_bbref: str, season: int
    ) -> pd.DataFrame:
        return PybaseballClient.fetch_batting_splits_leaderboards(player_bbref, season)

    def fetch_fangraphs_batter_data(
        self, player_name: str, team_fangraphs_id: str, start_year: int, end_year: int
    ):
        return PybaseballClient.fetch_fangraphs_batter_data(
            player_name, team_fangraphs_id, start_year, end_year
        )

    def fetch_statcast_batter_data(
        self, player_id: int, start_date: str, end_date: str
    ):
        try:
            return PybaseballClient.fetch_statcast_batter_data(
                player_id, start_date, end_date
            )
        except Exception as e:
            logger.info(f"Error fetching Statcast data for player {player_id}: {e}")
            return pd.DataFrame()

    def fetch_team_batting_stats(
        self, team_abbrev: str, start_year: int, end_year: int
    ):
        return PybaseballClient.fetch_team_batting_stats(
            team_abbrev, start_year, end_year
        )

    def save_statcast_batter_data(
        self, player_id: int, year: int, file_path: str = None
    ):
        return PybaseballClient.save_statcast_batter_data(player_id, year, file_path)

    def fetch_fangraphs_pitcher_data(
        self, player_name: str, team_fangraphs_id: str, start_year: int, end_year: int
    ):
        return PybaseballClient.fetch_fangraphs_pitcher_data(
            player_name, team_fangraphs_id, start_year, end_year
        )

    def fetch_pitching_splits_leaderboards(
        self, player_bbref: str, season: int
    ) -> pd.DataFrame:
        return PybaseballClient.fetch_pitching_splits_leaderboards(player_bbref, season)

    def fetch_statcast_pitcher_data(
        self, pitcher_id: int, start_date: str, end_date: str
    ):
        return PybaseballClient.fetch_statcast_pitcher_data(
            pitcher_id, start_date, end_date
        )

    def fetch_team_pitching_stats(
        self, team_abbrev: str, start_year: int, end_year: int
    ):
        return PybaseballClient.fetch_team_pitching_stats(
            team_abbrev, start_year, end_year
        )

    def save_statcast_pitcher_data(
        self, player_id: int, year: int, file_path: str = None
    ):
        return PybaseballClient.save_statcast_pitcher_data(player_id, year, file_path)

    def fetch_team_schedule_and_record(self, team_abbrev: str, season: int):
        return PybaseballClient.fetch_team_schedule_and_record(team_abbrev, season)

    #############################
    # WebClient wrappers
    #############################
    def fetch_logo_img(self, logo_url: str):
        return WebClient.fetch_logo_img(logo_url)

    def fetch_player_headshot(self, player_id: int):
        return WebClient.fetch_player_headshot(player_id)

    #############################
    # Player search wrappers
    #############################
    def lookup_player(self, last_name: str, first_name: str, fuzzy: bool = False):
        return self.search_client.playerid_lookup(
            last_name, first_name, ignore_accents=True, fuzzy=fuzzy
        )

    def lookup_player_by_id(self, player_id: int):
        return self.search_client.playerid_reverse_lookup([player_id], key_type="mlbam")

    def playerid_reverse_lookup(self, player_id, key_type="mlbam"):
        return self.search_client.playerid_reverse_lookup([player_id], key_type="mlbam")

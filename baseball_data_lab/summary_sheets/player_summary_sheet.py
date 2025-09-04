"""Base classes for player summary sheets."""

from baseball_data_lab.player.player import Player
from baseball_data_lab.apis.unified_data_client import UnifiedDataClient

from .base_sheet import BaseSheet


class PlayerSummarySheet(BaseSheet):
    """Shared initialization logic for player summary sheets."""

    def __init__(
        self,
        player: Player,
        season: int,
        data_client: UnifiedDataClient | None = None,
    ) -> None:
        """Initialize the sheet and load player data.

        Parameters
        ----------
        player:
            The :class:`~baseball_data_lab.player.player.Player` this sheet is for.
        season:
            The season for which to create the summary.
        data_client:
            Optional :class:`~baseball_data_lab.apis.unified_data_client.UnifiedDataClient`
            instance used to fetch data. A default client is created when ``None``.
        """

        super().__init__(season, data_client)
        self.player = player
        self.player.load_stats_for_season(season)
        self.player.load_statcast_data(self.start_date, self.end_date)


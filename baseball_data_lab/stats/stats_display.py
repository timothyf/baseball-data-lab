# Standard library imports
import matplotlib.pyplot as plt

# Application-specific imports
from baseball_data_lab.config.stats import StatsConfig
from baseball_data_lab.data_viz.stats_table import StatsTable
from baseball_data_lab.player.player import Player
from baseball_data_lab.apis.mlb_stats_client import process_splits


class StatsDisplay:
    def __init__(self, player: Player, season: int, stat_type: str):
        self.player = player
        self.stat_type = stat_type
        self.season_stats = StatsConfig().stat_lists[stat_type]


    def display_standard_stats(self, ax: plt.Axes):
        """Display standard statistics for the player."""
        self._display_stats(ax, "standard", "Standard")


    def display_advanced_stats(self, ax: plt.Axes):
        """Display advanced statistics for the player."""
        self._display_stats(ax, "advanced", "Advanced")


    def plot_splits_stats(self, ax: plt.Axes):
        if self.player.player_splits_stats is None:
            print("No splits stats data available.")
            return

        splits_data = self.player.player_splits_stats
        # The Stats API returns a list of split dictionaries.  ``StatsTable``
        # expects a ``DataFrame`` when generating a table, so convert the list
        # to a properly-indexed ``DataFrame`` when necessary.
        if isinstance(splits_data, list):
            splits_data = process_splits(splits_data)

        self._plot_stats_table(
            splits_data, self.season_stats["splits"], ax, "Splits", is_splits=True
        )


    # def _plot_stat_data(self, data, stat_type: str, ax: plt.Axes, title: str):
    #     if data is None:
    #         print(f"No {stat_type} stats data available.")
    #         return

    #     filtered_data = self._get_filtered_data(data, stat_type)
    #     if filtered_data is None or filtered_data.empty:
    #         print(f"No valid {stat_type} stats available for plotting.")
    #         return

    #     self._plot_stats_table(filtered_data, self.season_stats, ax, title, is_splits=False)


    # def _get_filtered_data(self, data, stat_type):
    #     """Retrieves and filters data based on `stat_type`."""
    #     season_data = data.get('season') or next(iter(data.values()))
    #     stats_df = pd.DataFrame([season_data])

    #     #return self._filter_columns(self.season_stats[stat_type], stats_df)
    #     return self._filter_columns(self.season_stats, stats_df)

    

    def _display_stats(self, ax: plt.Axes, stat_type: str, title: str):
        """Common workflow for displaying season statistics."""
        data = self.player.player_stats

        if data is None:
            print(f"No {stat_type} stats data available.")
            return

        stats_df = data
        filtered_data = self._filter_columns(self.season_stats[stat_type], stats_df)

        if filtered_data is None or filtered_data.empty:
            print(f"No valid {stat_type} stats available for plotting.")
            return

        self._plot_stats_table(filtered_data, self.season_stats[stat_type], ax, title, is_splits=False)


    def _plot_stats_table(self, stats, stat_fields, ax, title=None, is_splits=False):
        stats_table = StatsTable(stats, stat_fields, self.stat_type)
        stats_table.create_table(ax, f"{title} {self.stat_type.capitalize()}", is_splits)

    
    def _filter_columns(self, stat_fields, dataframe):
        """
        Filters the DataFrame to keep only the available columns from stat_fields.
        Handles missing columns gracefully.
        """
        missing_columns = [col for col in stat_fields if col not in dataframe.columns]
        
        if missing_columns:
            print(f"Warning: The following columns are missing from the DataFrame: {missing_columns}")
            available_columns = [col for col in stat_fields if col in dataframe.columns]

            if not available_columns:
                return None  # No valid columns available
            
            newDataframe = dataframe[available_columns]
        else:
            newDataframe = dataframe[stat_fields]

        return newDataframe.reset_index(drop=True)

        

import os
import pandas as pd

from baseball_data_lab.config.paths import DATA_DIR


class DataConverter:
    """Utility class for converting CSV data to JSON and generating team data."""

    def __init__(self, input_dir: str = DATA_DIR, output_dir: str = DATA_DIR):
        self.input_dir = input_dir
        self.output_dir = output_dir

    def csv_to_json(self, csv_filename: str, json_filename: str):
        """Convert a CSV file to a JSON Lines file."""
        csv_path = os.path.join(self.input_dir, csv_filename)
        json_path = os.path.join(self.output_dir, json_filename)

        try:
            df = pd.read_csv(csv_path)
        except FileNotFoundError:
            print(f"CSV file not found: {csv_path}")
            return
        except pd.errors.EmptyDataError:
            print(f"CSV file is empty: {csv_path}")
            return

        df.to_json(json_path, orient="records", lines=True)
        print(f"File converted and saved as JSON: {json_path}")

    def create_current_teams_json(self):
        """Create a JSON Lines file of current teams from a Fangraphs CSV file."""
        teams_csv = os.path.join(self.input_dir, "fangraphs_teams.csv")
        teams_json = os.path.join(self.output_dir, "current_teams.json")

        teams_df = pd.read_csv(teams_csv)
        teams_df = teams_df[teams_df["yearID"] == 2021]
        teams_df = teams_df[
            [
                "ID",
                "yearID",
                "lgID",
                "teamID",
                "franchID",
                "teamIDfg",
                "teamIDBR",
                "teamIDretro",
            ]
        ]
        teams_df.to_json(teams_json, orient="records", lines=True)
        print(f"Current teams JSON created: {teams_json}")

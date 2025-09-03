import os

STATS_API_BASE_URL = "https://statsapi.mlb.com/api/v1/"
SAVANT_BASE_URL = "https://baseballsavant.mlb.com/"
FANGRAPHS_BASE_URL = "https://www.fangraphs.com/api/leaders/major-league/data"
FANGRAPHS_NEXT_URL = "https://www.fangraphs.com/_next/data/Gtd7iofF2h1X98b-Nerh6/players"
MLB_STATIC_BASE_URL = "https://img.mlbstatic.com/mlb-photos/image/"
MLB_INFRA_BASE_URL = "https://bdfed.stitch.mlbinfra.com/bdfed/"

# Set BASE_DIR to the project root (baseball-data-lab directory)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))

# Now you can correctly build paths relative to the project root
DATA_DIR = os.path.join(BASE_DIR, 'baseball_data_lab', 'data')

# Statcast Data output directory
STATCAST_DATA_DIR = os.path.join(BASE_DIR, 'output')

# Player sheets output directory
PLAYER_SHEETS_DIR = os.path.join(BASE_DIR, 'output')

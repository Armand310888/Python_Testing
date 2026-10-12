import json
from pathlib import Path

from server import create_app


DATA_DIR = Path(__file__).resolve().parent


with open(DATA_DIR / 'clubs.json') as clubs_file:
    clubs = json.load(clubs_file)

with open(DATA_DIR / 'competitions.json') as competitions_file:
    competitions = json.load(competitions_file)

app = create_app(
    config=None,
    competitions=competitions,
    clubs=clubs,
    bookings=None,
)

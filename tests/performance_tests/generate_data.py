import json

from pathlib import Path

DATA_DIR = (
    Path(__file__).resolve().parent.parent / 'data/performance/'
)

clubs = [
    {
        "name": f"Performance Club {i}",
        "email": f"club{i}@example.com",
        "points": "120"
    }
    for i in range(1, 11)
]

competitions = [
    {
        "name": f"Performance Competition {i}",
        "date": "2100-01-01 10:00:00",
        "numberOfPlaces": "120"
    }
    for i in range(1, 11)
]

with open(DATA_DIR / 'clubs.json', 'w') as clubs_file:
    json.dump(clubs, clubs_file, indent=4)

with open(DATA_DIR / 'competitions.json', 'w') as competitions_file:
    json.dump(competitions, competitions_file, indent=4)

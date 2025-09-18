import json
from pathlib import Path

CORE_DIR = Path(__file__).resolve().parents[1]
SOURCES_FILE = CORE_DIR / 'omni' / 'utils' / 'sources.json'

def load_source_sites():
    with open(SOURCES_FILE, 'r') as file:
        data = json.load(file)
        return data


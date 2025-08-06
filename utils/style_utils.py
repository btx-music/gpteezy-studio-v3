import json
import os

PRESETS_PATH = "data/style_adlib_fx_presets.json"

def get_available_styles():
    if not os.path.exists(PRESETS_PATH):
        return []
    with open(PRESETS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        return list(data.keys())


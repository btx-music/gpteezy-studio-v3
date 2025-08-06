import json
import os

PRESETS_PATH = "data/voice_presets.json"

def load_preset_field(field_name, fallback=None):
    if not os.path.exists(PRESETS_PATH):
        return fallback
    try:
        with open(PRESETS_PATH, "r", encoding="utf-8") as f:
            presets = json.load(f)
            return presets.get(field_name, fallback)
    except Exception as e:
        print(f"[Preset Load Error]: {e}")
        return fallback

def load_presets():
    if not os.path.exists(PRESETS_PATH):
        return {}
    try:
        with open(PRESETS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[Preset Load Error]: {e}")
        return {}

def save_presets(presets):
    try:
        with open(PRESETS_PATH, "w", encoding="utf-8") as f:
            json.dump(presets, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[Preset Save Error]: {e}")

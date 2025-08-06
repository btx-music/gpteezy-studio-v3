# 🔧 Imports
import json
import random
import os

# 📂 Pfad zur Preset-Datei
PRESETS_PATH = "data/style_adlib_fx_presets.json"

# 1️⃣ Funktion zum Laden der Presets
def load_style_presets():
    if not os.path.exists(PRESETS_PATH):
        return {}
    with open(PRESETS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# 2️⃣ Funktion zur Anwendung der FX + Adlibs
def inject_fx_and_adlibs(lyrics, voice_style="Seductive_Male_EN", style="RnB"):
    presets = load_style_presets()
    style_presets = presets.get(style, {})
    adlibs = style_presets.get("adlibs", ["(yeah)", "(uh)"])
    fx_tags = style_presets.get("fx", ["[FX: Echo]", "[FX: Reverb]"])

    lines = lyrics.split("\n")
    new_lines = []
    for line in lines:
        if line.strip():
            if random.random() < 0.4:
                line += " " + random.choice(adlibs)
            if random.random() < 0.3:
                line += " " + random.choice(fx_tags)
        new_lines.append(line)

    return "\n".join(new_lines)

# 3️⃣ ➕ NEU: Verfügbare Styles auslesen
def get_available_styles():
    presets = load_style_presets()
    return list(presets.keys())

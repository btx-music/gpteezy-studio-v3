# voice_presets_tab.py (neu erstellen oder in voice_tab.py integrieren)
import streamlit as st
import json
import os

PRESETS_PATH = "data/voice_presets.json"

# Preset laden
def load_presets():
    if not os.path.exists(PRESETS_PATH):
        return []
    with open(PRESETS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# Preset speichern
def save_presets(presets):
    with open(PRESETS_PATH, "w", encoding="utf-8") as f:
        json.dump(presets, f, ensure_ascii=False, indent=2)

# Optional: Voreingestellte Vorschläge
PRESET_STYLES = [
    "Seductive_Male_DE", "Contemporary_Male_DE",
    "Seductive_Male_EN", "Contemporary_Male_EN"
]

def render_voice_presets_tab():
    st.header("🎚️ Voice Presets GUI")
    st.caption("Wähle, erstelle oder speichere deine Lieblings-KI-Stimmen")

    presets = load_presets()

    # Auswahl eines vorhandenen Presets
    selected = st.selectbox("🎙️ Preset wählen:", presets + ["🆕 Neues Preset erstellen"])

    if selected != "🆕 Neues Preset erstellen":
        st.success(f"Aktuelles Preset: {selected}")
    else:
        new_preset = st.text_input("✏️ Namen für neues Preset eingeben")
        if st.button("✅ Speichern"):
            if new_preset and new_preset not in presets:
                presets.append(new_preset)
                save_presets(presets)
                st.success(f"Preset '{new_preset}' gespeichert!")
            else:
                st.warning("Preset existiert bereits oder kein Name eingegeben")

    # Optional: Alle Presets anzeigen
    if st.checkbox("🔍 Alle gespeicherten Presets anzeigen"):
        st.code(json.dumps(presets, indent=2, ensure_ascii=False))

    # Optional: Preset löschen
    if presets:
        to_delete = st.selectbox("🗑️ Preset löschen:", presets)
        if st.button("Löschen"):
            presets.remove(to_delete)
            save_presets(presets)
            st.warning(f"Preset '{to_delete}' wurde entfernt")

    st.caption("💾 Gespeichert in: `data/voice_presets.json`")

import streamlit as st
from utils.preset_manager import load_presets, save_presets
import json

def render_instrumental_tab():
    st.header("🎼 AI Instrumental Generator")
    st.markdown("Erstelle **Suno-kompatible** Instrumental‑Prompts – garantiert **ohne Vocals**.")

    # 🔹 Mood-Presets
    mood_presets = {
        "Chill": {
            "genre": "Lo‑Fi",
            "instruments": "soft Rhodes piano, mellow bass, gentle drums",
            "fx": "warm reverb, light vinyl crackle"
        },
        "Happy": {
            "genre": "Funky Pop",
            "instruments": "electric guitar, groovy bass, upbeat drums",
            "fx": "bright reverb, slap delay"
        },
        "Euphoric": {
            "genre": "Deep House",
            "instruments": "sidechain pads, sub bass, punchy kick",
            "fx": "wide stereo reverb, airy delay"
        },
        "Dark": {
            "genre": "Trap",
            "instruments": "808 bass, dark synth pads, hi‑hat rolls",
            "fx": "deep reverb, distortion"
        },
        "Romantic": {
            "genre": "R&B",
            "instruments": "soft keys, smooth strings, warm bass",
            "fx": "plate reverb, soft delay"
        },
        "Dreamy": {
            "genre": "Ambient",
            "instruments": "airy synths, soft pads, slow percussion",
            "fx": "shimmer reverb, tape delay"
        },
        "Energetic": {
            "genre": "House",
            "instruments": "plucky synths, pumping bass, punchy drums",
            "fx": "sidechain compression, bright reverb"
        },
        "Sad": {
            "genre": "Lo‑Fi RnB",
            "instruments": "soft piano, mellow bass, lo‑fi drums",
            "fx": "lowpass filter, warm tape saturation"
        }
    }

    # 🔹 Genre-Liste (House jetzt enthalten)
    genre_list = ["RnB", "Pop", "HipHop", "Trap", "Deep House", "House", "Lo‑Fi", "Ambient", "Synthwave"]

    # 🔹 Mood-Verknüpfung – falls Mood Tab schon etwas ausgewählt hat
    linked_mood = st.session_state.get("selected_mood")  # kommt aus mood_tab.py

    if linked_mood and linked_mood in mood_presets:
        # Falls Mood im Instrumental-Tab neu ist oder noch keine Werte gespeichert → auto-füllen
        if linked_mood != st.session_state.get("inst_mood"):
            st.session_state["inst_mood"] = linked_mood
            st.session_state["inst_genre"] = mood_presets[linked_mood]["genre"]
            st.session_state["inst_instruments"] = mood_presets[linked_mood]["instruments"]
            st.session_state["inst_fx"] = mood_presets[linked_mood]["fx"]

    # 🔹 Letzte Werte oder Auto-Presets laden
    last_mood = st.session_state.get("inst_mood", "Chill")
    last_genre = st.session_state.get("inst_genre", mood_presets[last_mood]["genre"])
    last_tempo = st.session_state.get("inst_tempo", 100)
    last_key = st.session_state.get("inst_key", "C Major")
    last_instruments = st.session_state.get("inst_instruments", mood_presets[last_mood]["instruments"])
    last_fx = st.session_state.get("inst_fx", mood_presets[last_mood]["fx"])

    # 🔹 Mood-Auswahl
    mood = st.selectbox("🎭 Stimmung", list(mood_presets.keys()), index=list(mood_presets.keys()).index(last_mood))

    # Auto-Update wenn Mood wechselt
    if mood != last_mood:
        st.session_state["inst_genre"] = mood_presets[mood]["genre"]
        st.session_state["inst_instruments"] = mood_presets[mood]["instruments"]
        st.session_state["inst_fx"] = mood_presets[mood]["fx"]

    # 🔹 Genre-Auswahl mit sicherem Index (kein ValueError mehr)
    genre = st.selectbox(
        "🎵 Genre",
        genre_list,
        index=genre_list.index(last_genre) if last_genre in genre_list else 0
    )

    tempo = st.slider("⏱ Tempo (BPM)", 60, 180, last_tempo)

    key = st.selectbox(
        "🎼 Key",
        ["C Major", "G Major", "A Minor", "D Minor", "E Minor", "F Minor"],
        index=["C Major", "G Major", "A Minor", "D Minor", "E Minor", "F Minor"].index(last_key)
    )

    instruments = st.text_area("🎹 Instrumente / Sounds", st.session_state.get("inst_instruments", last_instruments))
    fx = st.text_area("✨ FX & Effekte", st.session_state.get("inst_fx", last_fx))

    # 🔹 Prompt generieren
    if st.button("✨ Instrumental‑Prompt generieren"):
        prompt = f"{genre} instrumental only, {mood} mood, {tempo} BPM, key {key}, featuring {instruments}, with {fx}, no vocals"

        # Speichern
        st.session_state["instrumental_prompt"] = prompt
        st.session_state["inst_genre"] = genre
        st.session_state["inst_mood"] = mood
        st.session_state["inst_tempo"] = tempo
        st.session_state["inst_key"] = key
        st.session_state["inst_instruments"] = instruments
        st.session_state["inst_fx"] = fx

        st.success("✅ Instrumental Prompt erstellt!")

        # 📋 Anzeige
        st.markdown("**📋 Generated Prompt:**")
        st.code(prompt)

        # Download .txt
        st.download_button("⬇️ Prompt als .txt speichern", prompt, file_name="instrumental_prompt.txt")

        # 🎧 Suno Export
        suno_export = {
            "title": "Instrumental Track",
            "prompt": prompt,
            "vocals": False,
            "genre": genre,
            "mood": mood,
            "tempo": tempo,
            "key": key,
            "instruments": instruments,
            "fx": fx
        }
        suno_json = json.dumps(suno_export, indent=2, ensure_ascii=False)
        st.download_button(
            "🎧 Suno Export (.json)",
            suno_json,
            file_name="instrumental_suno.json",
            mime="application/json"
        )

        # ➡️ In Songwriter übernehmen
        if st.button("📤 Prompt ins Songwriter‑Tab übernehmen"):
            st.session_state["voice_prompt"] = prompt
            st.session_state["active_tab"] = "🎤 Songwriter"
            st.session_state["force_switch"] = True
            st.rerun()

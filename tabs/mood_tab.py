import streamlit as st
from config import get_client, api_status, api_error_msg

def render_mood_tab():
    if not api_status:
        st.error(api_error_msg)
        st.stop()

    st.header("🧬 AI Mood Selector")
    st.markdown("Wähle einen **Song‑Mood** und entscheide, ob du nur Style & FX übernimmst, "
                "direkt Lyrics generierst oder ein passendes Instrumental erstellen willst.")

    # 🔹 Mood-Datenbank
    moods = {
        "Chill": {"style": "Lo‑Fi RnB", "fx": "soft vinyl crackle, warm reverb"},
        "Happy": {"style": "Funky Pop", "fx": "bright synths, claps, upbeat bass"},
        "Euphoric": {"style": "Deep House", "fx": "sidechain pads, punchy kick, airy leads"},
        "Dark": {"style": "Trap", "fx": "808 bass, dark pads, glitch FX"},
        "Romantic": {"style": "R&B Ballad", "fx": "soft keys, smooth strings, gentle percussion"},
        "Dreamy": {"style": "Ambient Pop", "fx": "shimmer reverb, airy synths, slow beats"},
        "Energetic": {"style": "House", "fx": "pumping bass, plucky synths, sidechain compression"},
        "Sad": {"style": "Lo‑Fi RnB", "fx": "soft piano, mellow bass, lo‑fi drums"}
    }

    # 🔹 Letzte Auswahl merken
    last_mood = st.session_state.get("selected_mood", "Chill")
    selected_mood = st.selectbox("🎭 Stimmung auswählen", list(moods.keys()), index=list(moods.keys()).index(last_mood))
    st.session_state["selected_mood"] = selected_mood

    # 🔹 Style & FX
    style = moods[selected_mood]["style"]
    fx = moods[selected_mood]["fx"]

    st.markdown(f"**🎨 Empfohlener Style:** {style}")
    st.markdown(f"**✨ Typische FX:** {fx}")

    # 📤 Mood → Instrumental Auto‑Flow
    if st.button("🎼 Nur Style & FX übernehmen → Instrumental Generator"):
        # Speichert Mood-Daten auch für Instrumental-Tab
        st.session_state["inst_mood"] = selected_mood
        st.session_state["inst_genre"] = style.split(" ")[0] if style.split(" ")[0] else "RnB"
        st.session_state["inst_instruments"] = f"Instrumente passend zu {style}"
        st.session_state["inst_fx"] = fx

        # Wechselt direkt zum Instrumental-Tab
        st.session_state["active_tab"] = "🎼 Instrumental Generator"
        st.session_state["force_switch"] = True
        st.rerun()

    # 🎵 Kompletten Mood-Songtext generieren
    if st.button("🎶 Kompletten Mood‑Songtext generieren"):
        try:
            client = get_client()
            mood_prompt = f"Song im Stil von {style} mit {fx}, passend zur Stimmung '{selected_mood}'"

            gpt_prompt = f"""
            Erstelle einen vollständigen Songtext im Stil von {style}.
            Der Song soll die Stimmung **{selected_mood}** widerspiegeln.
            Verwende folgende FX: {fx}.
            Songstruktur:
            [Intro]
            [Verse 1]
            [Chorus]
            [Verse 2]
            [Chorus]
            [Bridge]
            [Chorus]
            [Outro]
            Füge passende (Adlibs) und [FX]-Tags ein.
            Thema: {selected_mood}
            """

            with st.spinner(f"🎶 GPTeezy schreibt einen {selected_mood}-Song..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "Du bist ein erfahrener Songwriter-KI-Assistent."},
                        {"role": "user", "content": gpt_prompt}
                    ],
                    temperature=0.85,
                    max_tokens=900
                )

            generated_lyrics = response.choices[0].message.content.strip()

            # Lyrics ins Songwriter-Tab übernehmen
            st.session_state["songwriter_lyrics"] = generated_lyrics
            st.session_state["voice_prompt"] = mood_prompt
            st.session_state["active_tab"] = "🎤 Songwriter"
            st.session_state["force_switch"] = True
            st.rerun()

        except Exception as e:
            st.error(f"❌ Fehler bei der Lyrics-Generierung: {e}")

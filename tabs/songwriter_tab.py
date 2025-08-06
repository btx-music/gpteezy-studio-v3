import streamlit as st
from config import api_status, api_error_msg, get_client
from langdetect import detect
from utils.preset_manager import load_presets, save_presets, load_preset_field
from utils.formatting import format_lyrics
from utils.fx_adlib_engine import get_available_styles
from logic.file_saver import save_to_txt
import json

def render_songwriter_tab(client=None):
    if not api_status:
        st.error(api_error_msg)
        st.stop()

    if client is None:
        try:
            client = get_client()
        except Exception as e:
            st.error(f"❌ API-Client konnte nicht geladen werden: {e}")
            return

    # Übernahme aus Chat-Tab oder Voice Prompt
    if "songwriter_lyrics" in st.session_state and st.session_state["songwriter_lyrics"]:
        default_prompt = st.session_state["songwriter_lyrics"]
    else:
        default_prompt = st.session_state.get("voice_prompt", "")

    styles = get_available_styles() or ["RnB"]
    default_style = load_preset_field("style", fallback=styles[0])
    try:
        default_index = styles.index(default_style)
    except ValueError:
        default_index = 0
    style = st.selectbox("🎵 Wähle deinen Style:", styles, index=default_index)

    st.header("🎤 Songwriter Generator")

    user_prompt = st.text_area(
        "🧠 Inhalt / Thema",
        placeholder="z.B. Love.exe glitcht unter meiner Haut...",
        value=default_prompt
    )

    if user_prompt.strip():
        try:
            lang_detected = detect(user_prompt)
            lang = "DE" if lang_detected == "de" else "EN"
        except:
            lang = "EN"
    else:
        lang = "EN"
    st.markdown(f"🌐 Erkannte Sprache: :blue[**{lang}**]")

    voice_style = st.selectbox("🗣️ KI-Stimmstil wählen", ["Seductive", "Contemporary"], index=0)
    enable_fx_adlibs = st.checkbox("**🧪 FX-Adlibs aktivieren**", value=True)

    preset_options = load_presets() or ["Seductive_Male_EN"]

    if "voice_preset" in st.session_state and st.session_state["voice_preset"] in preset_options:
        selected_preset = st.session_state["voice_preset"]
    else:
        suggested_preset = f"{voice_style}_Male_{lang}"
        if suggested_preset not in preset_options:
            preset_options.append(suggested_preset)
            save_presets(preset_options)
        selected_preset = suggested_preset
        st.session_state["voice_preset"] = suggested_preset

    selected_preset = st.selectbox(
        "🎲 Preset wählen (für Suno Voice)",
        preset_options,
        index=preset_options.index(selected_preset)
    )

    if st.button("🎼 Song generieren (GPTeezy Direct)"):
        if not user_prompt.strip():
            st.warning("Bitte ein Thema eingeben oder im Voice Prompt Generator aufnehmen.")
            return

        with st.spinner("🎶 GPTeezy schreibt deinen Song..."):
            try:
                fx_text = "mit passenden [FX]-Tags und (Adlibs)" if enable_fx_adlibs else "ohne FX/Adlibs"
                gpt_prompt = f"""
                Erstelle einen vollständigen Songtext im Stil von {style}.
                Der Song soll die Sprache {lang} haben und in folgender Struktur sein:
                [Intro]
                [Verse 1]
                [Chorus]
                [Verse 2]
                [Chorus]
                [Bridge]
                [Chorus]
                [Outro]
                Verwende dabei {fx_text}.
                Thema: {user_prompt}
                """

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "Du bist ein erfahrener Songwriter-KI-Assistent."},
                        {"role": "user", "content": gpt_prompt}
                    ],
                    temperature=0.8,
                    max_tokens=800
                )

                raw_lyrics = response.choices[0].message.content.strip()
                formatted_lyrics = format_lyrics(raw_lyrics)

            except Exception as e:
                st.error(f"❌ Fehler bei der Lyrics-Generierung: {e}")
                return

        st.success("✅ Song erfolgreich generiert!")

        # === 📱 Mobile-Optimierter Scrollbereich für Lyrics ===
        st.markdown("### 📝 Lyrics")
        st.markdown("""
            <div style='max-height: 70vh; overflow-y: auto; padding: 10px;
                        border-radius: 8px; background-color: #fafafa;'>
        """, unsafe_allow_html=True)

        st.markdown(formatted_lyrics)

        st.markdown("</div>", unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("💾 Speichern als .txt"):
                save_to_txt("Song", formatted_lyrics)
                st.info("Textdatei gespeichert!")

        with col2:
            st.download_button(
                "⬇️ Song herunterladen",
                formatted_lyrics,
                file_name="Song.txt"
            )

        with col3:
            suno_export = {
                "title": "Song",
                "lyrics": formatted_lyrics,
                "voice": selected_preset,
                "style": style,
                "lang": lang,
                "fx_enabled": enable_fx_adlibs
            }
            suno_json = json.dumps(suno_export, indent=2, ensure_ascii=False)
            st.download_button(
                "🎵 Suno Export (.json)",
                suno_json,
                file_name="song_suno.json",
                mime="application/json"
            )

        with col4:
            suno_prompt_text = f"""
Song Title: Song
Style: {style}
Language: {lang}
Voice: {selected_preset}
FX Enabled: {enable_fx_adlibs}

Lyrics:
{formatted_lyrics}
"""
            st.text_area(
                "📋 Suno Prompt (Copy & Paste)",
                suno_prompt_text.strip(),
                height=250
            )
            st.info("⚡ Einfach kopieren & direkt in Suno einfügen!")

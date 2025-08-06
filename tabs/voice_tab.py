import streamlit as st
from config import api_status, api_error_msg, get_client
from utils.voice_utils import transcribe_voice
from utils.preset_manager import load_presets, save_presets

def render_voice_tab():
    # 🛡️ API-Check
    if not api_status:
        st.error(api_error_msg)
        st.stop()

    # 📊 Sidebar‑Statusindikator
    with st.sidebar:
        st.markdown("### 🎛 Voice Prompt Status")
        current_mode = st.session_state.get("voice_mode", "🎯 Normal Mode")
        st.markdown(f"**🛠 Modus:** {current_mode}")
        st.markdown(f"**🎤 Prompt:** {st.session_state.get('voice_prompt', '—')}")
        st.markdown(f"**🎲 Preset:** {st.session_state.get('voice_preset', '—')}")
        st.markdown("---")

    st.header("🎙️ Voice Prompt Generator (Dual‑Mode)")
    st.markdown("Wähle zwischen **Normal Mode** (nur speichern) und **Turbo Mode** (direkt Song generieren).")

    # Modus-Auswahl speichern
    mode = st.radio("⚙️ Modus wählen:", ["🎯 Normal Mode", "⚡ Turbo Mode"])
    st.session_state["voice_mode"] = mode


    # Funktion: Preset setzen
    def set_voice_preset(lang_code):
        voice_style_default = "Seductive"
        suggested_preset = f"{voice_style_default}_Male_{lang_code}"
        presets = load_presets() or []
        if suggested_preset not in presets:
            presets.append(suggested_preset)
            save_presets(presets)
        st.session_state["voice_preset"] = suggested_preset

    # Funktion: GPTeezy Lyrics generieren
    def generate_lyrics(prompt, lang_code):
        client = get_client()
        style = "RnB"  # Default Style
        fx_text = "mit passenden [FX]-Tags und (Adlibs)"
        gpt_prompt = f"""
        Erstelle einen vollständigen Songtext im Stil von {style}.
        Der Song soll die Sprache {lang_code} haben und folgende Struktur besitzen:
        [Intro]
        [Verse 1]
        [Chorus]
        [Verse 2]
        [Chorus]
        [Bridge]
        [Chorus]
        [Outro]
        Verwende {fx_text}.
        Thema: {prompt}
        """
        with st.spinner("🎶 GPTeezy schreibt deinen Song..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Du bist ein erfahrener Songwriter-KI-Assistent."},
                    {"role": "user", "content": gpt_prompt}
                ],
                temperature=0.8,
                max_tokens=800
            )
        return response.choices[0].message.content.strip()

    # 🎯 NORMAL MODE → Nur speichern & Songwriter öffnen
    if mode == "🎯 Normal Mode":
        use_voice = st.checkbox("🎤 Mikrofon verwenden")
        user_prompt = ""
        detected_lang = ""

        if use_voice:
            if st.button("🎙️ Jetzt sprechen (Normal Mode)"):
                user_prompt, detected_lang = transcribe_voice()
                if user_prompt:
                    st.success(f"🎙️ Erkanntes Thema: {user_prompt}")
                else:
                    st.warning("⚠️ Keine Sprache erkannt.")
        else:
            user_prompt = st.text_input(
                "💡 Songthema / Prompt eingeben",
                value=st.session_state.get("voice_prompt", "")
            )

        if user_prompt.strip():
            st.session_state["voice_prompt"] = user_prompt
            st.session_state["voice_lang"] = detected_lang if detected_lang else "EN"
            set_voice_preset(st.session_state["voice_lang"])

            # Sofort zu Songwriter wechseln
            st.session_state["active_tab"] = "🎤 Songwriter"
            st.session_state["force_switch"] = True
            st.rerun()

    # ⚡ TURBO MODE → 1-Klick Aufnahme & direkt Song generieren
    else:
        if st.button("🔥 🎤 One‑Click Record & Generate"):
            try:
                st.info("🎙 Aufnahme läuft... bitte sprechen!")
                user_prompt, detected_lang = transcribe_voice()

                if not user_prompt:
                    st.warning("⚠️ Keine Sprache erkannt.")
                    st.stop()

                st.success(f"✅ Erkanntes Thema: {user_prompt}")
                st.session_state["voice_prompt"] = user_prompt
                st.session_state["voice_lang"] = detected_lang if detected_lang else "EN"
                set_voice_preset(st.session_state["voice_lang"])

                # GPTeezy Song generieren
                generated_lyrics = generate_lyrics(user_prompt, st.session_state["voice_lang"])
                st.session_state["songwriter_lyrics"] = generated_lyrics

                # Direkt zu Songwriter springen
                st.session_state["active_tab"] = "🎤 Songwriter"
                st.session_state["force_switch"] = True
                st.rerun()

            except Exception as e:
                st.error(f"❌ Fehler: {e}")

    # 🧹 Reset
    if st.button("♻️ Alles zurücksetzen"):
        st.session_state["voice_prompt"] = ""
        st.session_state["voice_preset"] = ""
        st.session_state["voice_lang"] = ""
        st.session_state["songwriter_lyrics"] = ""
        st.rerun()

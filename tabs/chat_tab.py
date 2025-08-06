import streamlit as st
from config import api_status, api_error_msg, get_client

def render_chat_tab():
    """
    💬 GPTeezy Songwriter Chat Tab (Mobile‑Scroll Optimized)
    - Speichert Chat-Verlauf in st.session_state.chat_history
    - Kann direkt komplette Songtexte schreiben
    - Übergabe an Songwriter-Tab per Button mit Auto-Switch
    """

    st.header("💬 Chat mit GPTeezy (Songwriter Mode)")

    # API-Status prüfen
    if not api_status:
        st.error(api_error_msg)
        st.stop()

    # Chat-Verlauf initialisieren
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Reset-Button
    if st.button("♻️ Verlauf löschen"):
        st.session_state.chat_history = []
        st.rerun()

    # Letzte GPTeezy-Antwort merken
    last_gpt_reply = None

    # === 📱 Mobile‑optimierter Scrollcontainer für Chatverlauf ===
    if st.session_state.chat_history:
        st.markdown("### 💬 Chatverlauf:")

        st.markdown("""
            <div style='max-height: 70vh; overflow-y: auto; padding: 10px;
                        border-radius: 8px; background-color: #f0f0f0;'>
        """, unsafe_allow_html=True)

        for role, message in st.session_state.chat_history:
            if role == "user":
                st.markdown(f"**🧑‍💻 Du:** {message}")
            else:
                st.markdown(f"**🎤 GPTeezy:** {message}")
                last_gpt_reply = message

        st.markdown("</div>", unsafe_allow_html=True)

    # Falls letzte Antwort Lyrics sind → Button anzeigen
    if last_gpt_reply:
        if st.button("🎼 In Songwriter-Tab übernehmen"):
            st.session_state["songwriter_lyrics"] = last_gpt_reply
            st.session_state["voice_prompt"] = last_gpt_reply
            st.session_state["active_tab"] = "🎤 Songwriter"  # exakter Tab-Name
            st.session_state["force_switch"] = True
            st.rerun()

    # Eingabe-Feld
    user_input = st.text_area("💬 Deine Nachricht oder Songidee", key="chat_input", height=80)

    # Nachricht senden
    if st.button("📨 Senden") and user_input.strip():
        client = get_client()

        # User Nachricht in Verlauf
        st.session_state.chat_history.append(("user", user_input))

        try:
            # GPTeezy API-Aufruf
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": """Du bist GPTeezy, ein kreativer KI‑Songwriter.
Schreibe auf Wunsch komplette Songtexte mit folgender Struktur:
[Intro]
[Verse 1]
[Chorus]
[Verse 2]
[Chorus]
[Bridge]
[Chorus]
[Outro]
Füge passende (Adlibs) und [FX]-Tags ein, um Stimmung und Effekte zu verstärken.
Antworte im gewünschten Stil (RnB, Pop, Rap, etc.) und in der Sprache, die der Nutzer verwendet."""
                    }
                ] + [
                    {"role": role, "content": msg}
                    for role, msg in st.session_state.chat_history
                ],
                temperature=0.85,
                max_tokens=900
            )

            gpt_reply = response.choices[0].message.content.strip()

        except Exception as e:
            gpt_reply = f"❌ Fehler: {e}"

        # GPT Antwort speichern
        st.session_state.chat_history.append(("assistant", gpt_reply))
        st.rerun()

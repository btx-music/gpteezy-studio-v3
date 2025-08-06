import streamlit as st

def show_voice_status():
    st.markdown("### 🎛 Voice Prompt Status")
    current_mode = st.session_state.get("voice_mode", "🎯 Normal Mode")
    st.markdown(f"**🛠 Modus:** {current_mode}")
    st.markdown(f"**🎤 Prompt:** {st.session_state.get('voice_prompt', '—')}")
    st.markdown(f"**🎲 Preset:** {st.session_state.get('voice_preset', '—')}")
    st.markdown("---")

    # 🧹 Prompt löschen-Button
    if st.button("🗑 Prompt löschen", key="clear_voice_prompt_sidebar"):
        st.session_state["voice_prompt"] = ""
        st.session_state["voice_preset"] = ""
        st.session_state["voice_lang"] = ""
        st.session_state["songwriter_lyrics"] = ""
        st.success("Voice Prompt zurückgesetzt!")

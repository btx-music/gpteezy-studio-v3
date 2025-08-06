import os
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st
import streamlit.components.v1 as components
import time
import base64
import tempfile

# 🔄 Environment laden
load_dotenv()

# 🔑 API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_PROJECT_ID = os.getenv("OPENAI_PROJECT_ID")

# 🛡️ API Status
api_status = True
api_error_msg = None
if not OPENAI_API_KEY:
    api_status = False
    api_error_msg = "❌ Fehlender OPENAI_API_KEY in .env"
if not OPENAI_PROJECT_ID:
    api_status = False
    if api_error_msg:
        api_error_msg += " | Fehlende OPENAI_PROJECT_ID"
    else:
        api_error_msg = "❌ Fehlende OPENAI_PROJECT_ID in .env"

def get_client():
    if not api_status:
        raise RuntimeError(api_error_msg)
    return OpenAI(api_key=OPENAI_API_KEY, project=OPENAI_PROJECT_ID)

# 🎼 Sound Optionen
SOUND_OPTIONS = {
    "🚀 Sci-Fi Whoosh": "https://actions.google.com/sounds/v1/impacts/metal_impact_ring.ogg",
    "🎯 Arcade Ping": "https://actions.google.com/sounds/v1/cartoon/clang_and_wobble.ogg",
    "🎹 Synth Sweep": "https://actions.google.com/sounds/v1/alarms/beep_short.ogg",
    "💨 Light Whoosh": "https://actions.google.com/sounds/v1/cartoon/wood_plank_flicks.ogg",
    "🎵 GPTeezy Signature (Custom URL)": None,
    "🎤 GPTeezy Signature (Recording)": None
}

# 📊 API Debug Info
def show_api_debug_info():
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔍 GPTeezy API-Status")
    if api_status:
        st.sidebar.success("✅ API verbunden")
        st.sidebar.write(f"**Projekt-ID:** `{OPENAI_PROJECT_ID}`")
        st.sidebar.write(f"**API-Key:** `{OPENAI_API_KEY[:6]}...***`")
    else:
        st.sidebar.error(api_error_msg)

# 🎚️ Soundauswahl & One‑Click Recorder
def select_flow_sound():
    st.sidebar.markdown("---")
    st.sidebar.subheader("🎧 Flow-Switch Sound")

    if "flow_sound" not in st.session_state:
        st.session_state["flow_sound"] = list(SOUND_OPTIONS.keys())[0]

    st.session_state["flow_sound"] = st.sidebar.selectbox("Sound auswählen:", list(SOUND_OPTIONS.keys()))

    # Custom URL Eingabe
    if st.session_state["flow_sound"] == "🎵 GPTeezy Signature (Custom URL)":
        st.session_state["flow_sound_url"] = st.sidebar.text_input(
            "🌐 Eigene Sound-URL (MP3/OGG)",
            value=st.session_state.get("flow_sound_url", "")
        ).strip()

    # One‑Click Aufnahme im Browser
    if st.session_state["flow_sound"] == "🎤 GPTeezy Signature (Recording)":
        st.sidebar.markdown("🎙 **Direkt im Browser aufnehmen:**")

        record_html = """
        <script>
        let chunks = [];
        let recorder;
        function startRecording() {
            navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
                recorder = new MediaRecorder(stream);
                chunks = [];
                recorder.ondataavailable = e => chunks.push(e.data);
                recorder.onstop = e => {
                    let blob = new Blob(chunks, { type: 'audio/ogg; codecs=opus' });
                    let reader = new FileReader();
                    reader.readAsDataURL(blob);
                    reader.onloadend = () => {
                        window.parent.postMessage({ type: 'AUDIO_REC', data: reader.result }, '*');
                    };
                };
                recorder.start();
                document.getElementById("status").innerHTML = "⏺ Aufnahme läuft...";
            });
        }
        function stopRecording() {
            recorder.stop();
            document.getElementById("status").innerHTML = "✅ Aufnahme beendet!";
        }
        </script>
        <button onclick="startRecording()">🎙 Start Aufnahme</button>
        <button onclick="stopRecording()">⏹ Stopp</button>
        <div id="status">⚪ Bereit zur Aufnahme</div>
        """
        components.html(record_html, height=120)

        # Falls Audio hochgeladen wird
        audio_file = st.sidebar.file_uploader("oder Datei hochladen (MP3/WAV/OGG)", type=["mp3", "wav", "ogg"])
        if audio_file is not None:
            tmp_path = os.path.join(tempfile.gettempdir(), f"gpt_eezy_signature.{audio_file.name.split('.')[-1]}")
            with open(tmp_path, "wb") as f:
                f.write(audio_file.read())
            st.session_state["flow_sound_path"] = tmp_path
            st.sidebar.audio(tmp_path)
            st.sidebar.success("🎤 Signature Sound gespeichert!")

# 🔊 Sound abspielen
def _play_switch_sound():
    choice = st.session_state.get("flow_sound", list(SOUND_OPTIONS.keys())[0])
    
    # Aufnahme abspielen
    if choice == "🎤 GPTeezy Signature (Recording)":
        file_path = st.session_state.get("flow_sound_path")
        if file_path and os.path.exists(file_path):
            with open(file_path, "rb") as f:
                b64_audio = base64.b64encode(f.read()).decode()
            st.markdown(
                f"""
                <audio autoplay>
                    <source src="data:audio/ogg;base64,{b64_audio}" type="audio/ogg">
                </audio>
                """,
                unsafe_allow_html=True
            )
            return
    
    # Custom URL abspielen
    if choice == "🎵 GPTeezy Signature (Custom URL)":
        sound_url = st.session_state.get("flow_sound_url", "")
    else:
        sound_url = SOUND_OPTIONS[choice]
    
    if sound_url:
        st.markdown(
            f"""
            <audio autoplay>
                <source src="{sound_url}" type="audio/ogg">
            </audio>
            """,
            unsafe_allow_html=True
        )

# 🔄 Progress Animation + Meldung
def _run_progress_animation(sidebar=True, main=False, switch_message=None):
    if sidebar:
        progress_placeholder_sb = st.sidebar.empty()
        progress_bar_sb = progress_placeholder_sb.progress(0)
    if main:
        progress_placeholder_main = st.empty()
        progress_bar_main = progress_placeholder_main.progress(0)

        if switch_message:
            st.markdown(
                f"""
                <div style='padding:12px; background-color:#222; color:#0f0; 
                            border-radius:8px; text-align:center; font-weight:bold; font-size:1.2em;
                            animation: fadeInOut 1.5s ease-in-out;'>
                    🚀 Switching Flow… {switch_message}
                </div>
                <style>
                    @keyframes fadeInOut {{
                        0% {{ opacity: 0; transform: translateY(-10px); }}
                        30% {{ opacity: 1; transform: translateY(0); }}
                        70% {{ opacity: 1; }}
                        100% {{ opacity: 0; transform: translateY(10px); }}
                    }}
                </style>
                """,
                unsafe_allow_html=True
            )

    for percent in range(0, 101, 10):
        if sidebar:
            progress_bar_sb.progress(percent)
        if main:
            progress_bar_main.progress(percent)
        time.sleep(0.05)

    time.sleep(0.05)
    if sidebar:
        progress_placeholder_sb.empty()
    if main:
        progress_placeholder_main.empty()

# 📊 Flow Tracker
def show_flow_tracker():
    select_flow_sound()
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔄 Voice → Songwriter Flow")

    has_prompt = bool(st.session_state.get("voice_prompt", "").strip())
    has_preset = bool(st.session_state.get("voice_preset", "").strip())

    st.sidebar.markdown("✅ **Schritt 1:** Voice Prompt vorhanden" if has_prompt else "⬜ **Schritt 1:** Voice Prompt fehlt")
    st.sidebar.markdown("✅ **Schritt 2:** Voice Preset gesetzt" if has_preset else "⬜ **Schritt 2:** Voice Preset fehlt")

    if has_prompt and has_preset:
        st.sidebar.markdown(
            """
            <div style='padding:6px; background-color:#E0FFE0; border-radius:6px; text-align:center;
                        font-weight:bold; animation: pulseReady 1.5s infinite;'>
                🟢 Flow Status: Bereit zum Generieren 🎶
            </div>
            <style>
                @keyframes pulseReady {
                    0% { transform: scale(1); opacity: 0.8; }
                    50% { transform: scale(1.05); opacity: 1; }
                    100% { transform: scale(1); opacity: 0.8; }
                }
            </style>
            """,
            unsafe_allow_html=True
        )

        col_a, col_b = st.sidebar.columns(2)
        with col_a:
            if st.button("↩️ Songwriter"):
                _play_switch_sound()
                _run_progress_animation(sidebar=True, main=True, switch_message="🎤 Voice → ✍️ Songwriter")
                st.session_state["active_tab"] = "🎤 Songwriter"
                st.experimental_rerun()
        with col_b:
            if st.button("🎤 Voice"):
                _play_switch_sound()
                _run_progress_animation(sidebar=True, main=True, switch_message="✍️ Songwriter → 🎤 Voice")
                st.session_state["active_tab"] = "🎤 Voice Prompt Generator"
                st.experimental_rerun()
    else:
        st.sidebar.markdown("⚪ **Flow Status:** Noch nicht bereit")

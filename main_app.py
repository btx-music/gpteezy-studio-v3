import streamlit as st
from config import (
    get_client,
    show_api_debug_info,
    api_status,
    api_error_msg,
    show_flow_tracker
)

# 🎯 Tabs importieren
from tabs.songwriter_tab import render_songwriter_tab
from tabs.voice_tab import render_voice_tab
from tabs.instrumental_tab import render_instrumental_tab
from tabs.mood_tab import render_mood_tab
from tabs.chat_tab import render_chat_tab
from tabs.voice_presets_tab import render_voice_presets_tab
from utils.sidebar_status import show_voice_status

# 🖥 App-Konfiguration
st.set_page_config(page_title="Studio 3.0 - B:TX Edition", layout="wide")
st.title("🎤 Studio 3.0 - B:TX Edition")

# 📱 Mobile-Friendly + Feinschliff CSS
st.markdown("""
    <style>
    /* ===== Responsive Sidebar (App Navigation Style) ===== */
    @media (max-width: 768px) {
        section[data-testid="stSidebar"] {
            width: 160px !important;
            min-width: 160px !important;
            background-color: #1E1E1E !important;
        }
        section[data-testid="stSidebar"] .css-1d391kg {
            display: block !important;
        }
    }
    [data-testid="stSidebar"] .stRadio label {
        display: flex;
        align-items: center;
        padding: 8px 10px;
        border-radius: 8px;
        font-size: 15px;
        color: white !important;
        gap: 8px;
    }
    [data-testid="stSidebar"] .stRadio label:hover {
        background-color: #333333 !important;
    }
    [data-testid="stSidebar"] .stRadio [aria-checked="true"] label {
        background-color: #FFD43B !important;
        color: black !important;
        font-weight: bold;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.3);
    }

    /* ===== Buttons Mobile-Friendly ===== */
    @media (max-width: 768px) {
        .stButton > button {
            font-size: 18px !important;
            padding: 14px 20px !important;
            margin-top: 5px !important;
            margin-bottom: 5px !important;
            width: 100% !important;
        }
    }

    /* ===== Floating Action Buttons ===== */
    .fab {
        position: fixed;
        bottom: 15px;
        z-index: 99;
        border-radius: 50%;
        padding: 12px 14px;
        font-size: 20px;
        cursor: pointer;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.3);
    }
    .fab-main { right: 15px; background: #FF6B6B; color: white; }
    .fab-scroll { right: 70px; background: #FFE066; color: black; }

    /* ===== Inputs Mobile-Friendly ===== */
    @media (max-width: 768px) {
        textarea, input, select {
            font-size: 16px !important;
        }
    }

    /* ===== Auto-Switch Highlight Animation ===== */
    @keyframes fadeout {
        0%   { opacity: 1; }
        70%  { opacity: 1; }
        100% { opacity: 0; display:none; }
    }
    </style>
""", unsafe_allow_html=True)

# 📊 API Debug Info in Sidebar anzeigen
show_api_debug_info()

# 🎛 Voice Prompt Status immer anzeigen
with st.sidebar:
    show_voice_status()

# 🎚 Flow-Tracker
show_flow_tracker()

# 🔄 Aktiven Tab initialisieren
if "active_tab" not in st.session_state:
    st.session_state["active_tab"] = "🎤 Songwriter"

# 📌 Einheitliche Tab-Beschriftungen
tab_labels = [
    "🎤 Songwriter",
    "📜 Voice Presets",
    "🎙 Voice Prompter",
    "🎼 Instrumental Generator",
    "🧬 Mood Selector",
    "💬 Chat mit GPTeezy"
]

# 🎯 Auto-Switch Highlight Trigger
if "highlight_tab" not in st.session_state:
    st.session_state["highlight_tab"] = None

# Sidebar-Auswahl mit Auto-Switch
if st.session_state.get("force_switch", False):
    menu = st.session_state["active_tab"]
    st.session_state["force_switch"] = False
    st.session_state["highlight_tab"] = menu
else:
    active_name = st.session_state["active_tab"]
    if active_name not in tab_labels:
        active_name = "🎤 Songwriter"
    menu = st.sidebar.radio("📂 Tabs", tab_labels, index=tab_labels.index(active_name))

# Auswahl speichern
st.session_state["active_tab"] = menu

# 🎨 Smooth Highlight-Effekt anzeigen (nur einmal)
if st.session_state["highlight_tab"] == menu:
    st.markdown(
        f"""
        <div style="
            padding:10px;
            background-color:#FFE066;
            border-radius:8px;
            text-align:center;
            font-weight:bold;
            font-size:1.1em;
            animation: fadeout 3s ease-in-out forwards;
        ">
            🚀 Automatisch gewechselt zu: {menu}
        </div>
        """,
        unsafe_allow_html=True
    )
    st.session_state["highlight_tab"] = None

# 🎤 Floating Button „Zurück zum Songwriter“ (nur wenn nicht im Songwriter-Tab)
if st.session_state.get("active_tab") != "🎤 Songwriter":
    if st.button("🎤", key="fab_songwriter", help="Zurück zum Songwriter"):
        st.session_state["active_tab"] = "🎤 Songwriter"
        st.session_state["force_switch"] = True
        st.rerun()

# ⬆ Scroll-to-Top Button – final funktionierend & smooth
st.markdown("""
    <style>
    .scroll-top-btn {
        position: fixed;
        bottom: 15px;
        right: 70px;
        z-index: 999;
        background-color: #FFE066;
        color: black;
        border: none;
        border-radius: 50%;
        padding: 10px 14px;
        font-size: 20px;
        cursor: pointer;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.3);
    }
    </style>

    <script>
    function scrollToTop() {
        window.scrollTo({top: 0, behavior: 'smooth'});
    }
    </script>

    <button class="scroll-top-btn" onclick="scrollToTop()" title="Nach oben scrollen">⬆</button>
""", unsafe_allow_html=True)

# Tabs rendern
if menu == "🎤 Songwriter":
    if api_status:
        render_songwriter_tab()
    else:
        st.error(api_error_msg)

elif menu == "📜 Voice Presets":
    render_voice_presets_tab()

elif menu == "🎙 Voice Prompter":
    render_voice_tab()

elif menu == "🎼 Instrumental Generator":
    render_instrumental_tab()

elif menu == "🧬 Mood Selector":
    render_mood_tab()

elif menu == "💬 Chat mit GPTeezy":
    render_chat_tab()

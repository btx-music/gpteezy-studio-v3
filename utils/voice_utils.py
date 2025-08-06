import streamlit as st
import speech_recognition as sr

def transcribe_voice():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        st.info("🎙️ Bitte sprich jetzt... (Deutsch oder Englisch möglich)")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # Auto-Erkennung mit Google Speech
    try:
        st.success("✅ Stimme erkannt – wird transkribiert...")
        # Versuche zuerst Deutsch
        text = recognizer.recognize_google(audio, language="de-DE")
        lang = "DE"
    except sr.UnknownValueError:
        try:
            # Fallback: Englisch
            text = recognizer.recognize_google(audio, language="en-US")
            lang = "EN"
        except sr.UnknownValueError:
            st.error("❌ Sprache konnte nicht erkannt werden.")
            return "", None
        except sr.RequestError as e:
            st.error(f"❌ API-Fehler (EN): {e}")
            return "", None
    except sr.RequestError as e:
        st.error(f"❌ API-Fehler (DE): {e}")
        return "", None

    return text, lang

# logic/lyrics_generator.py
from config import get_client
from utils.fx_adlib_engine import inject_fx_and_adlibs

def generate_lyrics(system_prompt, style, voice, lang, enable_fx_adlibs=False):
    client = get_client()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Schreibe einen Song im Stil von {style}."}
    ]

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.9
    )

    full_output = response.choices[0].message.content.strip()

    # Optional: Songtitel extrahieren (wenn z. B. erste Zeile „Titel: …“ ist)
    if full_output.lower().startswith("titel:"):
        title_line, *lyrics_lines = full_output.split("\n", 1)
        title = title_line.replace("Titel:", "").strip()
        lyrics = "\n".join(lyrics_lines).strip()
    else:
        title = "Untitled"
        lyrics = full_output

    # ✨ Optional: FX & Adlibs injizieren
    if enable_fx_adlibs:
        lyrics = inject_fx_and_adlibs(lyrics, voice_style=voice, style=style)

    return lyrics, title

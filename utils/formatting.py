import re

def format_lyrics(lyrics):
    # Runde Klammern durch eckige ersetzen für Songstruktur
    pattern = r"\((Verse|Chorus|Bridge|Intro|Outro|Drop|Pre-Chorus)\)"
    return re.sub(pattern, r"[\1]", lyrics)

import os

def save_to_txt(title, content):
    os.makedirs("exports", exist_ok=True)
    with open(f"exports/{title}.txt", "w", encoding="utf-8") as f:
        f.write(content)

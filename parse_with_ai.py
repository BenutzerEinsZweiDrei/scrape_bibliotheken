import requests, json
from g4f.client import Client

def get_answer(text):
    client = Client()
    response = client.chat.completions.create(
        model="deepseek-v3",
        messages=[{"role": "user", "content": text}],
        web_search=True
    )
    return response.choices[0].message.content


def parse_ai_to_md():
    # --- Read data from urls.json ---
    with open("urls.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    def answer_for_urls(urls):
        # send to g4f
        linkstext = " ".join(urls)
        prompt = """
        
        Im folgenden bekommst du urls von einer Bibliotheks Seite.
        Bitte durchsuche diese Webseiten, ob in dieser Bibliothek eine >Online< Anmeldung möglich ist,
        also die Beantragung eines Bibliotheks Ausweis über das Internet,
        oder nur vor Ort in der Bibliothek.
        
        Zusätzlich scanne die urls nach Informationen zu Kosten des Bibliotheksausweis
        und weiteren Ansprüchen an potenzielle Kunden (wie bspw Wohnort etc).
        
        Alle urls sind von ein und derselben Bibliothek,
        also scanne erst alle urls und
        anschließend triff im Folgenden deine Bewertung.
        Also nur eine Gesamtbewertung.
        
        Bitte verzichte in deiner Antwort auf Erklärungen.
        
        Antworte nur im folgenden Format:
        
        
        Anmeldung Online oder Offline:
            "Online"  (wenn eine online Anmeldung möglich ist)
            "Offline" (wenn nur offline Anmeldung möglich ist)
            "keine Informationen" (wenn du dazu keine Informatoinen gefunden hast)
        
        Kosten des Bibliotheksausweis: (Nenne hier den Preis.)
        
        Weitere Informationen: (Nenne weitere relevante Informationen)
        
        Jetzt kommen die urls:
        
        """
        prompt =  prompt + linkstext
        
        try:
            return get_answer(prompt)
        except Exception as e:
            print(f"Fehler aufgetreten.")

    md_lines = []
    
    for entry in data:
        source = entry.get("source_url", "")
        urls = entry.get("matched_urls", [])
        
        information = answer_for_urls(urls)
        
        md_lines.append(f"## [{source}]({source})\n")
        if information:
            md_lines.append(f"{information}\n")
        md_lines.append("")  # blank line between entries
        
        print("Finished url: ", source)
        print("Information: ", information)
        
        
    return "\n".join(md_lines)
        


# --- Generate Markdown ---
markdown_output = parse_ai_to_md()

# --- Save to libraries.md ---
with open("libraries.md", "w", encoding="utf-8") as f:
    f.write(markdown_output)

print("✅ Markdown file 'libraries.md' created successfully!")
"""
AI-gestützte Analyse von Bibliothekswebseiten.

Dieses Skript verwendet ein AI-Modell (über g4f), um die von keyword_spider
gesammelten URLs zu analysieren und wichtige Informationen zu extrahieren:
- Online vs. Offline Anmeldung
- Kosten des Bibliotheksausweises
- Weitere relevante Informationen (z.B. Wohnsitzanforderungen)

Eingabe: urls.json (von keyword_spider generiert)
Ausgabe: libraries.md (strukturierte Markdown-Datei mit Ergebnissen)

Voraussetzungen:
    - g4f Python-Paket (pip install g4f)
    - urls.json im aktuellen Verzeichnis
    - Internetverbindung für AI-Modell-Zugriff

Verwendung:
    python parse_with_ai.py

Hinweis: 
    - Das Skript nutzt Web-Suche für bessere Ergebnisse
    - Jede Bibliothek wird einzeln verarbeitet (kann dauern)
    - Bei Fehlern wird eine Fehlermeldung ausgegeben, aber die Verarbeitung fortgesetzt
"""

import requests, json
from g4f.client import Client

def get_answer(text):
    """
    Sendet eine Anfrage an das AI-Modell und erhält eine Antwort.
    
    Verwendet das deepseek-v3 Modell über den g4f Client mit aktivierter
    Web-Suche für aktuelle und genaue Informationen.
    
    Args:
        text (str): Der Prompt/die Frage an das AI-Modell
        
    Returns:
        str: Die Antwort des AI-Modells
        
    Raises:
        Exception: Bei Verbindungsproblemen oder API-Fehlern
    """
    client = Client()
    response = client.chat.completions.create(
        model="deepseek-v3",
        messages=[{"role": "user", "content": text}],
        web_search=True  # Aktiviert Web-Suche für bessere Informationen
    )
    return response.choices[0].message.content


def parse_ai_to_md():
    """
    Hauptfunktion: Verarbeitet urls.json und erstellt libraries.md.
    
    Workflow:
    1. Lädt die URLs aus urls.json
    2. Für jede Bibliothek:
       - Erstellt einen detaillierten Prompt mit allen gefundenen URLs
       - Sendet den Prompt an das AI-Modell
       - Sammelt die strukturierte Antwort
    3. Erstellt eine Markdown-Datei mit allen Ergebnissen
    
    Returns:
        str: Der vollständige Markdown-Text mit allen Bibliotheksinformationen
        
    Raises:
        FileNotFoundError: Wenn urls.json nicht gefunden wird
        json.JSONDecodeError: Wenn urls.json ungültiges JSON enthält
    """
    # --- Read data from urls.json ---
    with open("urls.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    def answer_for_urls(urls):
        """
        Erstellt einen AI-Prompt und holt Antworten für eine Bibliothek.
        
        Der Prompt fordert das AI-Modell auf:
        - Alle URLs zu durchsuchen
        - Informationen zur Online-/Offline-Anmeldung zu finden
        - Kosten des Bibliotheksausweises zu ermitteln
        - Weitere relevante Bedingungen (z.B. Wohnsitz) zu erfassen
        
        Args:
            urls (list): Liste der zu analysierenden URLs einer Bibliothek
            
        Returns:
            str: Strukturierte Antwort vom AI-Modell oder None bei Fehler
        """
        # URLs als Leerzeichen-getrennte Liste zusammenfügen
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
            # Bei Fehler wird eine Meldung ausgegeben, aber das Skript läuft weiter
            print(f"Fehler aufgetreten.")

    md_lines = []
    
    # Verarbeite jede Bibliothek einzeln
    for entry in data:
        source = entry.get("source_url", "")
        urls = entry.get("matched_urls", [])
        
        # Hole AI-Antwort für diese Bibliothek
        information = answer_for_urls(urls)
        
        # Erstelle Markdown-Eintrag mit Überschrift und Link zur Website
        md_lines.append(f"## [{source}]({source})\n")
        if information:
            md_lines.append(f"{information}\n")
        md_lines.append("")  # Leerzeile zwischen Einträgen
        
        # Fortschritt ausgeben
        print("Finished url: ", source)
        print("Information: ", information)
        
        
    return "\n".join(md_lines)
        


# --- Generate Markdown ---
markdown_output = parse_ai_to_md()

# --- Save to libraries.md ---
with open("libraries.md", "w", encoding="utf-8") as f:
    f.write(markdown_output)

print("✅ Markdown file 'libraries.md' created successfully!")
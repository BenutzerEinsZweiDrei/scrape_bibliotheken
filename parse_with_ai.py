## consider preparsing
## downloading all urls with r.jina for a folder each
## rating each .md for relevance by keyword search or topic extraction
## maybe jina.ai classify
## summarizing relevant .mds for later analysis



import requests, os, shutil, re, json
from pathlib import Path
from colorama import init, Back, Fore
init(autoreset=True)

from ollama import chat
from ollama import ChatResponse

from openai import OpenAI

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="<YOUR OPENROUTER KEY>",
)





# === Einstellungen ===
INPUT_JSON = "urls.json"   # dein JSON-Dateiname
OUTPUT_DIR = "output"      # Hauptordner für alles
HEADERS = {"User-Agent": "Mozilla/5.0"}  # um blockierte Requests zu vermeiden

# === Hauptlogik ===
def get_all_md():
    # JSON laden
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Jede Source iterieren
    for idx, entry in enumerate(data, start=1):
        folder = Path(OUTPUT_DIR) / str(entry["idx"])
        folder.mkdir(exist_ok=True)
        print(f"[+] Ordner {folder} für {entry['source_url']}")

        for j, url in enumerate(entry.get("matched_urls", []), start=1):
            try:
                r = requests.get(f"https://r.jina.ai//{url}", headers=HEADERS, timeout=15)
                r.raise_for_status()
                # Datei speichern
                md_path = folder / f"page_{j}.md"
                with open(md_path, "w", encoding="utf-8") as out:
                    out.write(f"# {url}\n\n")
                    out.write(r.text)
                print(f"  ✔ Gespeichert: {md_path.name}")
            except Exception as e:
                print(f"  ✖ Fehler bei {url}: {e}")

def classify_all():
    def get_classify(text):
        url = 'https://api.jina.ai/v1/classify'
        headers = {
            "Content-Type": "application/json",
            "Authorization": "<YOUR JINA AI KEY>"
        }
        data = {
            "model": "jina-embeddings-v3",
            "input": [text],
            "labels": [
                "Anmelde-Informationen",
                "Ausweis-Informationen",
                "Keine Informationen"
            ]
        }
        try:
            response = requests.post(url, headers=headers, json=data)
            # response.raise_for_status()
            result = response.json()
        except Exception:
            print("jina failed")
        
       # print(result)

        # Extrahiere das wahrscheinlichste Label (abhängig vom API-Output)
        try:
            label = result["data"][0]["prediction"]
        except Exception:
            label = "Unbekannt"

        return label

    base_folder = "output"
    # classify_folder = "classified"

    # rekursiv alle .md-Dateien sammeln
    md_files = []
    for root, dirs, files in os.walk(base_folder):
        for file in files:
            if file.endswith(".md"):
                md_files.append(os.path.join(root, file))

    # liste filtern
    md_files_filtered = [entry for entry in md_files if "Unbekannt" in entry]
    # print(len(md_files_filtered))
    
    for file_path in md_files_filtered:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        # Dateiinhalt klassifizieren
        label = get_classify(text)
        print(f"{file_path} → {label}")
        
        # split file_path
        file_path_reduced = os.path.join(file_path.split("\\")[0], file_path.split("\\")[1])

        # Zielordner erstellen
        target_dir = os.path.join(file_path_reduced, label)
        os.makedirs(target_dir, exist_ok=True)

        # Datei verschieben
        filename = os.path.basename(file_path)
        target_path = os.path.join(target_dir, filename)
        shutil.move(file_path, target_path)

        print(f"✔️ Datei verschoben nach: {target_path}")
        
def delete_for_keyword():
    
    base_folder = "output"
    
    md_files = []
    
    # rekursiv alle .md Dateien sammeln
    for root, dirs, files in os.walk(base_folder):
        for file in files:
            if file.endswith(".md"):
                md_files.append(os.path.join(root, file))
                
                
    # liste filtern
    # md_files_filtered = [entry for entry in md_files if "Anmelde" in entry or "Ausweis" in entry]
    # print(len(md_files_filtered))
    
    
    keywords = ["anmeldung", "benutzung", "registierung", "ausweis", "karte", "kosten"]
    
    for file_path in md_files:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        
        if not any(kw in text for kw in keywords):
            # remove file
            os.remove(file_path)
            print("File deleted ", file_path)
            
       
 
def summarize_mds():

    
    
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

        

        completion = client.chat.completions.create(
          extra_headers={
            "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
            "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
          },
          model="openai/gpt-4o",
          messages=[
            {
              "role": "user",
              "content": text
            }
          ]
        )

        return completion.choices[0].message.content
    
    
    
    base_folder = "scrape/output"
    
    md_files = []
    
    # rekursiv alle .md Dateien sammeln
    for root, dirs, files in os.walk(base_folder):
        for file in files:
            if file.endswith(".md"):
                md_files.append(os.path.join(root, file))
                
                
    # liste filtern
    md_files_filtered = [entry for entry in md_files if "Extraktion" in entry]
    print(len(md_files_filtered))
    
    for file_path in md_files_filtered:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
            
            
        prompt = """
        
                    Findest du hier Informationen zu:
                    
                    - Anmeldung Online oder nur Offline?
                    - Kosten des Bibliotheksausweis?
                    - Weitere Hinweise zur Beantragen und Ansprüche wie bspw Wohnort, Alter etc. ?
                    
                    Antworte bitte kurz.
                    
                    Falls du keine Hinweise findest antworte mit "hier keine Hinweise".
                    
                    Suche die Informationen im folgenden Text:
                    
                    ==== 
        
        """
        
        prompt = prompt + text
        
        try:
            result = get_answer(prompt)
            print(Back.GREEN + "Got Answer")
            with open(file_path, "w", encoding="utf-8") as out:
                    out.write(result)
                    print(f"  ✔ Gespeichert: {file_path}")
        except Exception:
            print(Back.RED + "Prompt Failed")
    

def extract_parts():
    
    # === Konfiguration ===
    
    base_folder = "scrape/output"
    
    md_files = []
    
    # rekursiv alle .md Dateien sammeln
    for root, dirs, files in os.walk(base_folder):
        for file in files:
            if file.endswith(".md"):
                md_files.append(os.path.join(root, file))
                
                
    # liste filtern
    input_path_list = [entry for entry in md_files if "Anmelde" in entry or "Ausweis" in entry]
    print(len(input_path_list))
    

    # Liste der Suchbegriffe (Groß-/Kleinschreibung ignorieren)
    KEYWORDS = ["anmeldung", "benutzung", "registierung", "ausweis", "karte", "kosten"]

    # === Hilfsfunktionen ===
    def split_markdown_sections(text: str):
        """
        Zerlegt den Markdown-Text in Abschnitte anhand von Überschriften
        oder Leerzeilen. Gibt eine Liste von Abschnitten (Strings) zurück.
        """
        # Abschnittstrennung durch 2+ Zeilenumbrüche
        sections = re.split(r"\n{2,}", text.strip())
        return [sec.strip() for sec in sections if sec.strip()]

    def extract_sections_with_keywords(sections, keywords):
        """
        Durchsucht Abschnitte nach Keywords (case-insensitive)
        und gibt alle Abschnitte zurück, die mindestens ein Keyword enthalten.
        """
        matched = []
        for x, sec in enumerate(sections, start=0):
            for kw in keywords:
                if re.search(rf"\b{re.escape(kw)}\b", sec, re.IGNORECASE):
                    if x>0 and x<len(sections)-1:
                        matched.append(sections[x-1]+sections[x]+sections[x+1])
                    else:
                        matched.append(sec)
                    break
        return matched

    def save_markdown(sections, output_path):
        """Speichert gefundene Abschnitte in eine Markdown-Datei."""
        with open(output_path, "w", encoding="utf-8") as f:
            for sec in sections:
                f.write(sec + "\n\n---\n\n")

    # === Hauptlogik ===
    def main_here():
        
        
        
        for idx, input_path in enumerate(input_path_list, start=1):
        
            file_path = input_path
            
            with open(input_path, "r", encoding="utf-8") as f:
                text = f.read()

            sections = split_markdown_sections(text)
            extracted = extract_sections_with_keywords(sections, KEYWORDS)

            if extracted:
                        
                # create output path
                output_root = os.path.join(file_path.split("\\")[0], file_path.split("\\")[1])
                output_dir = Path("Extraktion")
                output_dir = os.path.join(output_root, output_dir)
                os.makedirs(output_dir, exist_ok=True)
                
                output_path = output_dir +"/"+ f"extraktion_{idx}.md"
                save_markdown(extracted, output_path)
                print(f"✅ {len(extracted)} relevante Abschnitte extrahiert -> {output_path}")
            else:
                print("⚠️ Keine Treffer gefunden.")
    
    # run logic
    main_here()


def merge_mds():
    base_folder = "scrape/output"
    
    md_files = []
    
    # rekursiv alle .md Dateien sammeln
    for root, dirs, files in os.walk(base_folder):
        for file in files:
            if file.endswith(".md"):
                md_files.append(os.path.join(root, file))
                
                
    # liste filtern
    md_files_filtered = [entry for entry in md_files if "Extraktion" in entry]
    print(len(md_files_filtered))
    
    
    # liste sortieren
    md_files_sorted = {}
    for entry in md_files_filtered:
        root = os.path.join(entry.split("\\")[0], entry.split("\\")[1])
        folder = os.path.join(root, entry.split("\\")[2])
        path = os.path.join(folder, entry.split("\\")[3])
        if Path(root) not in md_files_sorted:
            md_files_sorted[Path(root)] = []
        md_files_sorted[Path(root)].append(Path(path))
    
    print(md_files_sorted)
    
    for root, entry in md_files_sorted.items():
        
        md_text = ""
        
        for file in entry:
            with open(file, "r", encoding="utf-8") as f:
                text = f.read()
                
            md_text += text + "\n\n"
            
        with open(Path(os.path.join(root, "merged.md")), "w", encoding="utf-8") as f:
                f.write(md_text)
                
        print(f"Finished {root}")
           
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
    
    base_folder = "scrape/output"
    
    md_files = []
    
    # rekursiv alle .md Dateien sammeln
    for root, dirs, files in os.walk(base_folder):
        for file in files:
            if file.endswith(".md"):
                md_files.append(os.path.join(root, file))
                
                
    # liste filtern
    md_files_filtered = [entry for entry in md_files if "merged" in entry]
    print(len(md_files_filtered))
    
    
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

        

        completion = client.chat.completions.create(
          extra_headers={
            "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
            "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
          },
          model="openai/gpt-4o",
          messages=[
            {
              "role": "user",
              "content": text
            }
          ]
        )

        return completion.choices[0].message.content
                    
            
        
        
        
        
        
        
    def answer_for_urls(entry):
        
        with open(entry, "r", encoding="utf-8") as f:
            text = f.read()
        
        
        
        # refactor this prompt 
        prompt = """"
        
                    Extrahiere aus den folgenden Texten Informationen zu einer Bibliothek:
                    
                    - Anmeldung Online oder nur Offline?
                    - Kosten des Bibliotheksausweis?
                    - Weitere Hinweise zur Beantragen und Ansprüche wie bspw Wohnort, Alter etc.?
                    
                    Antworte bitte sehr kurz und nur mit diesen Hinweisen.
                    
                    Falls du keine Hinweise findest antworte mit "hier keine Hinweise".
                    
                    Im folgenden die Texte 
                    
                    ==== 
                    
                    
                    """
        prompt =  prompt + text
        
        try:
            return get_answer(prompt)
        except Exception as e:
            # Bei Fehler wird eine Meldung ausgegeben, aber das Skript läuft weiter
            print(Back.RED + "Fehler aufgetreten.")

    md_lines = []
    
    with open("scrape/urls.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        
    # Verarbeite jede Bibliothek einzeln
    for entry in md_files_filtered:

        # hole source aus urls.json
        for eintrag in data:
            if int(entry.split("\\")[1]) == eintrag["idx"]:
                source = eintrag["source_url"]
                break
        
        
        # Hole AI-Antwort für diese Bibliothek
        information = answer_for_urls(entry)
        
        # Erstelle Markdown-Eintrag mit Überschrift und Link zur Website
        md_lines.append(f"## [{source}]({source})\n")
        if information:
            md_lines.append(f"{information}\n")
        md_lines.append("")  # Leerzeile zwischen Einträgen
        
        # Fortschritt ausgeben
        print(Back.GREEN + "Finished url: ", source)
        
        
    return "\n".join(md_lines)
        

def final_md():
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

        

        completion = client.chat.completions.create(
          extra_headers={
            "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
            "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
          },
          model="openai/gpt-4o",
          messages=[
            {
              "role": "user",
              "content": text
            }
          ]
        )

        return completion.choices[0].message.content


    # --- Generate Markdown ---
    markdown_output = parse_ai_to_md()

    # --- Save to libraries.md ---
    with open("libraries.md", "w", encoding="utf-8") as f:
        f.write(markdown_output)

    print("✅ Markdown file 'libraries.md' created successfully!")

    prompt = """

    Sortiere und Gruppiere die folgende Liste.

    Sende als Antwort ein beautiful markdown.

    """

    polished_output = get_answer(prompt + markdown_output)

    # --- Save to polished.md ---
    with open("polished.md", "w", encoding="utf-8") as f:
        f.write(polished_output)

    print("✅ Markdown file 'polished.md' created successfully!")
    
if __name__ == "__main__":
    # get_all_md()
    # delete_for_keyword()
    # classify_all()
    # extract_parts() # rework keywords
    # summarize_mds()
    # merge_mds()
    # final_md()

# scrape_bibliotheken

Ein Scrapy-basiertes Tool zum automatisierten Sammeln von Informationen über deutsche Stadtbibliotheken, insbesondere zu Anmeldeverfahren, Kosten und Nutzungsbedingungen.

## Projektbeschreibung

Dieses Projekt nutzt Scrapy-Spiders und KI-gestützte Analyse, um systematisch Informationen über die Anmeldung bei deutschen Stadtbibliotheken zu sammeln. Der Workflow umfasst:
1. Crawlen der Wikipedia-Liste deutscher Stadtbibliotheken
2. Durchsuchen der Bibliothekswebseiten nach relevanten Informationen
3. AI-gestützte Analyse zur Extraktion strukturierter Daten

## Voraussetzungen

- **Python**: Version 3.8 oder höher
- **pip**: Python-Paketmanager
- **Virtualenv** (optional, aber empfohlen)
- **Scrapy**: Version 2.13.3 oder höher
- **g4f**: Für die AI-gestützte Analyse
- **Internetverbindung**: Für Web-Scraping und AI-Modell-Zugriff

## Installation

### 1. Repository klonen

```bash
git clone https://github.com/BenutzerEinsZweiDrei/scrape_bibliotheken.git
cd scrape_bibliotheken
```

### 2. Virtuelle Umgebung erstellen (empfohlen)

```bash
# Virtuelle Umgebung erstellen
python -m venv venv

# Aktivieren (Linux/Mac)
source venv/bin/activate

# Aktivieren (Windows)
venv\Scripts\activate
```

### 3. Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

Die wichtigsten Abhängigkeiten sind:
- `scrapy>=2.13.3`: Web-Scraping-Framework
- `g4f`: AI-Model-Client für die Textanalyse

## Projektstruktur

```
scrape_bibliotheken/
├── scrape_bibliotheken/          # Hauptpaket
│   ├── spiders/                  # Scrapy-Spiders
│   │   ├── get_wikipedia.py      # Crawlt Wikipedia für Bibliotheksinfos
│   │   └── keyword_spider.py     # Sucht relevante URLs auf Bibliotheksseiten
│   ├── settings.py               # Scrapy-Konfiguration
│   ├── items.py                  # Datenmodelle (aktuell nicht aktiv genutzt)
│   ├── pipelines.py              # Datenverarbeitungs-Pipelines
│   └── middlewares.py            # Request/Response-Middlewares
├── parse_with_ai.py              # AI-gestützte Analyse der gesammelten URLs
├── requirements.txt              # Python-Abhängigkeiten
├── scrapy.cfg                    # Scrapy-Projektkonfiguration
├── example_output/               # Beispiel-Ausgabedateien
│   ├── bibliotheken.json         # Beispiel: Bibliotheksliste von Wikipedia
│   ├── urls.json                 # Beispiel: Gefundene URLs mit Keywords
│   └── libraries.md              # Beispiel: AI-analysierte Ergebnisse
└── README.md                     # Diese Datei
```

## Verwendung

### Drei-Schritte-Workflow

#### Schritt 1: Wikipedia-Daten crawlen

Crawlt die Wikipedia-Liste deutscher Stadtbibliotheken und extrahiert Namen, Wikipedia-URLs und offizielle Websites:

```bash
python -m scrapy crawl get_wikipedia -o bibliotheken.json
```

**Ausgabe**: `bibliotheken.json`
- Enthält für jede Bibliothek: Name, Wikipedia-URL, Website-URL
- Beispielstruktur:
  ```json
  [
    {
      "name": "Stadtbibliothek Aachen",
      "wikipedia_url": "https://de.wikipedia.org/wiki/Stadtbibliothek_Aachen",
      "website": "http://www.stadtbibliothek-aachen.de"
    }
  ]
  ```

**Debugging**: Prüfen Sie `bibliotheken.json` auf fehlende URLs (`"website": null`):
```bash
# Mit jq (falls installiert)
jq '.[] | select(.website == null)' bibliotheken.json

# Oder manuell die Datei durchsehen
grep -n "null" bibliotheken.json
```

#### Schritt 2: Relevante URLs auf Bibliotheksseiten finden

Durchsucht jede Bibliothekswebsite nach Links mit relevanten Keywords (faq, anmeldung, ausleihe, etc.):

```bash
python -m scrapy crawl keyword_spider -o urls.json
```

**Ausgabe**: `urls.json`
- Enthält für jede Website alle gefundenen URLs mit Keywords
- Beispielstruktur:
  ```json
  [
    {
      "source_url": "http://www.stadtbibliothek-aachen.de",
      "matched_urls": [
        "http://www.stadtbibliothek-aachen.de/anmeldung",
        "http://www.stadtbibliothek-aachen.de/faq"
      ]
    }
  ]
  ```

**Debugging**: Prüfen Sie `urls.json` auf Bibliotheken ohne gefundene URLs:
```bash
# Mit jq (falls installiert)
jq '.[] | select(.matched_urls == ["keine gefunden"])' urls.json

# Anzahl der Bibliotheken ohne Ergebnisse
jq '[.[] | select(.matched_urls == ["keine gefunden"])] | length' urls.json
```

#### Schritt 3: AI-gestützte Analyse durchführen

Analysiert die gefundenen URLs mit einem AI-Modell und extrahiert strukturierte Informationen:

```bash
python parse_with_ai.py
```

**Ausgabe**: `libraries.md`
- Markdown-Datei mit strukturierten Informationen für jede Bibliothek:
  - Online vs. Offline Anmeldung
  - Kosten des Bibliotheksausweises
  - Weitere relevante Informationen (z.B. Wohnsitzbedingungen)

**Hinweis**: Dieser Schritt kann einige Zeit dauern, da jede Bibliothek einzeln analysiert wird. Der Fortschritt wird in der Konsole angezeigt.

### Beispiel-Workflow komplett

```bash
# Schritt 1
python -m scrapy crawl get_wikipedia -o bibliotheken.json
# Überprüfen: jq '.[] | select(.website == null)' bibliotheken.json

# Schritt 2
python -m scrapy crawl keyword_spider -o urls.json
# Überprüfen: jq '.[] | select(.matched_urls == ["keine gefunden"])' urls.json

# Schritt 3
python parse_with_ai.py
# Ergebnis ansehen: cat libraries.md
```

## AI-Nutzung und Umgebungsvariablen

### g4f (GPT4Free)

Dieses Projekt verwendet `g4f` für den Zugriff auf AI-Modelle ohne API-Schlüssel. Das Skript `parse_with_ai.py` nutzt:
- **Modell**: `deepseek-v3`
- **Web-Suche**: Aktiviert für aktuelle Informationen
- **Keine API-Keys erforderlich**: g4f funktioniert ohne Authentifizierung

### Rate Limiting

Da das Skript öffentliche AI-Dienste nutzt:
- Verarbeitung erfolgt sequenziell (eine Bibliothek nach der anderen)
- Bei Fehlern wird eine Meldung ausgegeben, aber die Verarbeitung fortgesetzt
- Bei wiederholten Fehlern: Wartezeit einbauen oder später erneut versuchen

## Testen und Verifizierung

### Manuelle Überprüfung

Da keine automatisierten Tests vorhanden sind, sollten Sie die Ergebnisse manuell überprüfen:

1. **bibliotheken.json überprüfen**:
   - Sind alle erwarteten Bibliotheken enthalten?
   - Haben die meisten Bibliotheken eine Website-URL?

2. **urls.json überprüfen**:
   - Wurden relevante URLs gefunden?
   - Gibt es zu viele "keine gefunden"-Einträge?

3. **libraries.md überprüfen**:
   - Sind die Informationen korrekt und strukturiert?
   - Entsprechen die Ergebnisse dem erwarteten Format?

### Beispiel-Ausgaben

Im Verzeichnis `example_output/` finden Sie Beispieldateien aus einem kompletten Durchlauf zur Orientierung.

## Architektur-Überblick

```
┌─────────────────────────────────────────────────────────────────┐
│                    Datenfluss-Diagramm                          │
└─────────────────────────────────────────────────────────────────┘

  Wikipedia                      get_wikipedia.py
  (Liste deutscher     ──────>   (Scrapy Spider)
  Stadtbibliotheken)                    │
                                        ▼
                              bibliotheken.json
                          (Name, Wikipedia-URL, Website)
                                        │
                                        ▼
  Bibliotheks-                keyword_spider.py
  Websites         ──────>    (Scrapy Spider)
                          (sucht Keywords: anmeldung, faq, etc.)
                                        │
                                        ▼
                                   urls.json
                        (Website + gefundene URLs mit Keywords)
                                        │
                                        ▼
                               parse_with_ai.py
                            (AI-Analyse mit g4f)
                                        │
                                        ▼
                                 libraries.md
                    (Strukturierte Informationen zu jeder Bibliothek)
```

## Troubleshooting

### Häufige Probleme und Lösungen

#### Problem: `FileNotFoundError: bibliotheken.json not found`
**Lösung**: Führen Sie zuerst Schritt 1 aus, um `bibliotheken.json` zu erstellen.

#### Problem: Spider crawlt nicht alle Seiten
**Lösung**: 
- Prüfen Sie die `ROBOTSTXT_OBEY`-Einstellung in den Spiders (ist auf `False` gesetzt)
- Überprüfen Sie Ihre Internetverbindung
- Manche Websites blockieren Bots - dies ist normal

#### Problem: `keyword_spider` findet zu wenige URLs
**Lösung**:
- Überprüfen Sie die Keywords in `keyword_spider.py` - ggf. weitere hinzufügen
- Manche Bibliotheken verwenden andere Begriffe (z.B. "Registrierung" statt "Anmeldung")

#### Problem: AI-Analyse schlägt fehl
**Lösung**:
- Überprüfen Sie Ihre Internetverbindung
- g4f-Dienst könnte temporär nicht verfügbar sein - später erneut versuchen
- Aktualisieren Sie das g4f-Paket: `pip install --upgrade g4f`

#### Problem: Zu viele gleichzeitige Requests
**Lösung**:
- Die Einstellungen in `settings.py` sind bereits konservativ (1 Request/Domain, 1s Delay)
- Bei Bedarf `DOWNLOAD_DELAY` erhöhen

## Beitragen

### Branching und Commits

1. **Branch erstellen**:
   ```bash
   git checkout -b feature/ihre-feature-beschreibung
   ```

2. **Commit-Konventionen**:
   - `feat:` für neue Features
   - `fix:` für Bugfixes
   - `docs:` für Dokumentationsänderungen
   - `refactor:` für Code-Umstrukturierungen

   Beispiel:
   ```bash
   git commit -m "feat: add support for Austrian libraries"
   ```

3. **Pull Request erstellen**:
   - Beschreiben Sie Ihre Änderungen klar und ausführlich
   - Fügen Sie Tests oder manuelle Verifikationsschritte hinzu
   - Verweisen Sie auf relevante Issues

### Code-Style

- Folgen Sie PEP 8 für Python-Code
- Docstrings im Google-Style-Format
- Kommentare auf Deutsch (konsistent mit bestehendem Code)
- Minimale Änderungen - nur notwendige Code-Modifikationen

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Siehe LICENSE-Datei für Details.

## Kontakt und Autor

- **Repository**: [BenutzerEinsZweiDrei/scrape_bibliotheken](https://github.com/BenutzerEinsZweiDrei/scrape_bibliotheken)
- **Issues**: Bitte verwenden Sie den GitHub Issue Tracker für Fehlerberichte und Feature-Anfragen

## Weitere Ressourcen

- [Scrapy-Dokumentation](https://docs.scrapy.org/)
- [g4f GitHub Repository](https://github.com/xtekky/gpt4free)
- [Wikipedia-Liste deutscher Stadtbibliotheken](https://de.wikipedia.org/wiki/Liste_deutscher_Stadtbibliotheken)

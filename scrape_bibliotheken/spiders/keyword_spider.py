"""
Keyword-Spider zum Durchsuchen von Bibliothekswebseiten.

Dieser Spider nimmt eine Liste von Bibliothekswebsites (aus bibliotheken.json)
und durchsucht diese nach Links mit bestimmten Schlüsselwörtern im Linktext,
die auf Anmelde- und Nutzungsinformationen hinweisen.

Keywords: faq, nutzung, ausleihe, anmeldung, mitglied, benutzung, ausweis

Output: JSON-Datei mit gefundenen URLs pro Bibliothek (urls.json)
"""

import scrapy
import json
from urllib.parse import urljoin, urlparse
import os

class KeywordSpider(scrapy.Spider):
    """
    Spider zum Durchsuchen von Bibliothekswebseiten nach relevanten Links.
    
    Dieser Spider:
    1. Lädt eine Konfigurationsdatei (bibliotheken.json) mit Website-URLs
    2. Crawlt jede Website und sucht nach Links mit spezifischen Keywords
    3. Sammelt alle passenden URLs für jede Bibliothek
    
    Suchstrategie:
        - Durchsucht alle <a>-Elemente mit href-Attribut
        - Prüft, ob der Linktext eines der definierten Keywords enthält
        - Sammelt alle gefundenen URLs pro Bibliothek
        
    Ausgabefelder:
        source_url (str): Die gescannte Bibliothekswebsite
        matched_urls (list): Liste aller gefundenen URLs mit Keywords
                             oder ["keine gefunden"] wenn nichts gefunden wurde
        
    Custom Settings:
        - USER_AGENT: Simuliert einen modernen Chrome-Browser
        - ROBOTSTXT_OBEY: False (um alle relevanten Seiten zu erreichen)
    """
    name = "keyword_spider"
    
    custom_settings = {
        "USER_AGENT": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/127.0.0.1 Safari/537.36"
        ),
        "ROBOTSTXT_OBEY": False,
    }
    
    # Keywords zum Suchen nach relevanten Informationen zu Anmeldung und Nutzung
    keywords = ["faq", "nutzung", "ausleihe", "anmeldung", "mitglied", "benutzung", "ausweis"]

    def __init__(self, config_file="bibliotheken.json", *args, **kwargs):
        """
        Initialisiert den Spider mit einer Konfigurationsdatei.
        
        Lädt die Bibliothekswebsites aus der JSON-Datei und erstellt die
        Liste der zu crawlenden Start-URLs sowie erlaubten Domains.
        
        Args:
            config_file (str): Pfad zur JSON-Konfigurationsdatei mit Bibliotheksdaten
            *args: Weitere positionelle Argumente für den Spider
            **kwargs: Weitere Keyword-Argumente für den Spider
            
        Raises:
            FileNotFoundError: Wenn die Konfigurationsdatei nicht existiert
            ValueError: Wenn keine gültigen Start-URLs in der Konfiguration gefunden wurden
        """
        super().__init__(*args, **kwargs)

        # Konfiguration aus JSON laden
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Config file '{config_file}' not found.")

        with open(config_file, "r", encoding="utf-8") as f:
            config = json.load(f)

        # Extrahiere alle Website-URLs aus der Konfiguration
        self.start_urls = [entry["website"] for entry in config if "website" in entry]
        # Entferne null/None-Werte aus der Liste
        self.start_urls = [entry for entry in self.start_urls if entry]
        # Extrahiere Domains für allowed_domains (Sicherheitsmaßnahme)
        self.allowed_domains = [urlparse(url).netloc for url in self.start_urls]


        if not self.start_urls:
            raise ValueError("No start_urls found in config file.")
            
    def parse(self, response):
        """
        Parst eine Bibliothekswebsite und sucht nach Links mit Keywords.
        
        Diese Methode durchsucht alle Links auf der Seite und sammelt diejenigen,
        deren Linktext mindestens eines der definierten Keywords enthält.
        
        Args:
            response: HTTP-Response der Bibliothekswebsite
            
        Yields:
            dict: Dictionary mit 'source_url' und 'matched_urls' Feldern
        """
        matched_urls = []  # Liste zum Sammeln aller passenden URLs

        # Alle <a>-Elemente mit href-Attribut finden
        for link in response.css("a[href]"):
            href = link.attrib.get("href")
            # Linktext extrahieren und in Kleinbuchstaben umwandeln für case-insensitive Suche
            link_text = (link.css("::text").get(default="") or "").strip().lower()

            # Prüfen, ob eines der Keywords im Linktext vorkommt
            if any(keyword in link_text for keyword in self.keywords):
                # Relative URLs zu absoluten URLs umwandeln
                full_url = urljoin(response.url, href)
                matched_urls.append(full_url)

        # Erst hier, nachdem alle gesammelt sind, yielden
        if matched_urls:
            yield {
                "source_url": response.url,
                "matched_urls": matched_urls  # alle gesammelt in einer Liste
            }
        else:
            # Wenn keine URLs gefunden wurden, trotzdem ein Ergebnis zurückgeben
            yield {
                "source_url": response.url,
                "matched_urls": ["keine gefunden"]
            }

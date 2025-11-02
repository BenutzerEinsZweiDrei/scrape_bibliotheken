import scrapy
import json
from urllib.parse import urljoin, urlparse
import os

class KeywordSpider(scrapy.Spider):
    name = "keyword_spider"
    
    idx = 0
    
    custom_settings = {
        "USER_AGENT": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; de-DE) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/128.0.6613.121 Safari/537.36"
        ),
        "DEFAULT_REQUEST_HEADERS": {
            "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
        },
        "ROBOTSTXT_OBEY": False,
    }
    
    # Keywords zum Suchen
    keywords = ["information", "service", "antworten", "antwort", "fragen", "frage", "faq", "nutzung", "ausleihe", "anmeldung", "mitglied", "benutzung", "ausweis"]

    def __init__(self, config_file="bibliotheken.json", *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Konfiguration aus JSON laden
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Config file '{config_file}' not found.")

        with open(config_file, "r", encoding="utf-8") as f:
            config = json.load(f)

        self.start_urls = [entry["website"] for entry in config if "website" in entry]
        self.start_urls = [entry for entry in self.start_urls if entry] ## remove null
        self.allowed_domains = [urlparse(url).netloc for url in self.start_urls]


        if not self.start_urls:
            raise ValueError("No start_urls found in config file.")
            
    def parse(self, response):
        matched_urls = []  # Liste zum Sammeln aller passenden URLs

        # Alle <a>-Elemente mit href finden
        for link in response.css("a[href]"):
            href = link.attrib.get("href")
            link_text = (link.css("::text").get(default="") or "").strip().lower()

            # Prüfen, ob eines der Keywords im Linktext oder im href vorkommt
            if (
                any(keyword in link_text for keyword in self.keywords)
                or any(keyword in href.lower() for keyword in self.keywords)
            ):
                full_url = urljoin(response.url, href)
                matched_urls.append(full_url)


        self.idx = self.idx + 1
        
        # Erst hier, nachdem alle gesammelt sind, yielden
        if matched_urls:
            yield {
                "idx": self.idx,
                "source_url": response.url,
                "matched_urls": matched_urls  # alle gesammelt in einer Liste
            }
        else:
            yield {
                "idx": self.idx,
                "source_url": response.url,
                "matched_urls": ["keine gefunden"]  # yield nothing found
            }

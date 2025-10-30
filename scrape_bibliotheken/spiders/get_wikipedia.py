"""
Wikipedia-Spider zum Sammeln von Bibliotheksinformationen.

Dieser Spider crawlt die Wikipedia-Seite "Liste deutscher Stadtbibliotheken"
und extrahiert für jede Bibliothek:
- Name der Bibliothek
- Wikipedia-URL
- Website-URL (falls vorhanden in der Infobox)

Output: JSON-Datei mit Bibliotheksinformationen (bibliotheken.json)
"""

import scrapy


class get_wikipedia(scrapy.Spider):
    """
    Spider zum Crawlen der Wikipedia-Liste deutscher Stadtbibliotheken.
    
    Dieser Spider:
    1. Startet auf der Wikipedia-Übersichtsseite für deutsche Stadtbibliotheken
    2. Folgt Links zu einzelnen Bibliotheks-Artikeln
    3. Extrahiert die offizielle Website aus der Infobox jedes Artikels
    
    Ausgabefelder:
        name (str): Name der Bibliothek aus Wikipedia
        wikipedia_url (str): URL des Wikipedia-Artikels
        website (str oder None): URL der offiziellen Bibliothekswebsite
        
    Custom Settings:
        - USER_AGENT: Simuliert einen modernen Chrome-Browser
        - ROBOTSTXT_OBEY: False (um alle Bibliotheksartikel zu erreichen)
    """
    name = "get_wikipedia"
    allowed_domains = ["de.wikipedia.org"]
    start_urls = ["https://de.wikipedia.org/wiki/Liste_deutscher_Stadtbibliotheken"]

    custom_settings = {
        "USER_AGENT": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/127.0.0.1 Safari/537.36"
        ),
        "ROBOTSTXT_OBEY": False,
    }

    def parse(self, response):
        """
        Parst die Wikipedia-Übersichtsseite und folgt Links zu Bibliotheksartikeln.
        
        Diese Methode extrahiert alle Links aus Listen-Elementen im Hauptinhalt
        und filtert irrelevante Links heraus (Bearbeitungs-Links, rote Links, Listen).
        
        Args:
            response: HTTP-Response der Wikipedia-Übersichtsseite
            
        Yields:
            scrapy.Request: Requests zu einzelnen Bibliotheks-Detailseiten
        """
        # Hauptinhalt der Wikipedia-Seite selektieren
        container = response.css("#mw-content-text > div.mw-content-ltr.mw-parser-output")

        for a in container.css("ul li a"):
            href = a.attrib.get("href")
            name = a.attrib.get("title")

            if not href:
                continue

            # Relative URLs zu absoluten URLs umwandeln
            if href.startswith("/"):
                href = response.urljoin(href)

            # Filter für irrelevante Links (Bearbeitungs-Links, nicht existierende Seiten, Listen)
            if "action=edit" in href or "redlink=1" in href or "Liste" in href:
                continue

            # Folge dem Link zur Detailseite der Bibliothek
            yield scrapy.Request(
                url=href,
                callback=self.parse_bibliothek,
                meta={"name": name, "wikipedia_url": href},
            )

    def parse_bibliothek(self, response):
        """
        Parst eine einzelne Bibliotheks-Detailseite und extrahiert die Website-URL.
        
        Sucht in der Wikipedia-Infobox nach dem "Website"-Feld und extrahiert
        die verlinkte URL. Die Infobox verwendet die ID "Vorlage_Infobox_Bibliothek".
        
        Args:
            response: HTTP-Response der Bibliotheks-Detailseite
            
        Yields:
            dict: Dictionary mit 'name', 'wikipedia_url' und 'website' Feldern
        """
        name = response.meta["name"]
        wikipedia_url = response.meta["wikipedia_url"]

        # Suche nach der Infobox (Vorlage_Infobox_Bibliothek)
        rows = response.css("#Vorlage_Infobox_Bibliothek > tbody > tr")

        website_url = None

        # Durchsuche alle Zeilen der Infobox nach dem "Website"-Feld
        for row in rows:
            th_text = row.css("th::text").get()
            if th_text and "Website" in th_text:
                website_url = row.css("td a::attr(href)").get()
                break

        # Relative URLs zu absoluten URLs umwandeln
        if website_url and website_url.startswith("/"):
            website_url = response.urljoin(website_url)

        yield {
            "name": name,
            "wikipedia_url": wikipedia_url,
            "website": website_url,
        }

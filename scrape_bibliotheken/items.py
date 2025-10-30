"""
Datenmodelle für gescrapte Bibliotheksinformationen.

Dieses Modul definiert Scrapy-Item-Klassen, die die Struktur der
gesammelten Daten beschreiben. Aktuell wird die Standard-Item-Klasse
verwendet, da die Spiders direkt Dictionaries zurückgeben.

Weitere Informationen:
https://docs.scrapy.org/en/latest/topics/items.html
"""

import scrapy


class ScrapeBibliothekenItem(scrapy.Item):
    """
    Basis-Item-Klasse für Bibliotheksinformationen.
    
    Diese Klasse kann erweitert werden, um strukturierte Felder
    für gescrapte Bibliotheksdaten zu definieren. Aktuell verwenden
    die Spiders direkt Dictionaries anstelle von Item-Objekten.
    """
    # Beispiel für mögliche Felder:
    # name = scrapy.Field()
    # website = scrapy.Field()
    # wikipedia_url = scrapy.Field()
    pass

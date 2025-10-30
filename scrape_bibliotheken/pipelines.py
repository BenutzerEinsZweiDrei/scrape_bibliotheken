"""
Item-Pipelines für die Verarbeitung gescrapter Bibliotheksdaten.

Dieses Modul definiert Pipelines, die die von Spiders gesammelten Items
verarbeiten, validieren, bereinigen oder in eine Datenbank schreiben können.

Um eine Pipeline zu aktivieren, muss sie in den ITEM_PIPELINES-Einstellungen
konfiguriert werden.

Weitere Informationen:
https://docs.scrapy.org/en/latest/topics/item-pipeline.html
"""

from itemadapter import ItemAdapter


class ScrapeBibliothekenPipeline:
    """
    Standard-Pipeline für Bibliotheksinformationen.
    
    Diese Pipeline führt aktuell keine Transformationen durch und gibt
    Items unverändert zurück. Sie kann erweitert werden für:
    - Validierung der Daten
    - Bereinigung/Normalisierung von URLs und Text
    - Speicherung in Datenbanken
    - Filterung von duplizierten Items
    """
    
    def process_item(self, item, spider):
        """
        Verarbeitet ein einzelnes Item aus einem Spider.
        
        Args:
            item: Das zu verarbeitende Item (Dictionary oder Item-Objekt)
            spider: Der Spider, der das Item erstellt hat
            
        Returns:
            Das verarbeitete Item (unverändert in der aktuellen Implementation)
        """
        return item

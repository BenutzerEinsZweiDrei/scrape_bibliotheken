"""
Spider- und Downloader-Middlewares für das Scrape-Bibliotheken-Projekt.

Dieses Modul enthält Middleware-Klassen, die den Request/Response-Zyklus
von Scrapy-Spiders beeinflussen können. Middlewares können verwendet werden für:
- Modifikation von Requests vor dem Senden
- Verarbeitung von Responses vor der Weitergabe an Spider
- Fehlerbehandlung und Retry-Logik
- Request-Header-Manipulation

Weitere Informationen:
https://docs.scrapy.org/en/latest/topics/spider-middleware.html
https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
"""

from scrapy import signals
from itemadapter import ItemAdapter


class ScrapeBibliothekenSpiderMiddleware:
    """
    Spider-Middleware für die Verarbeitung von Spider-Callbacks.
    
    Diese Middleware wird zwischen dem Scrapy-Engine und den Spider-Callbacks
    ausgeführt. Sie kann Responses vor der Verarbeitung durch den Spider
    modifizieren oder filtern.
    """
    
    @classmethod
    def from_crawler(cls, crawler):
        """
        Factory-Methode zum Erstellen der Middleware-Instanz.
        
        Diese Methode wird von Scrapy aufgerufen und ermöglicht den Zugriff
        auf Crawler-Einstellungen und Signals.
        
        Args:
            crawler: Die Scrapy-Crawler-Instanz
            
        Returns:
            Eine neue Instanz der Middleware
        """
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        """
        Verarbeitet Responses, bevor sie an den Spider weitergeleitet werden.
        
        Args:
            response: Das Response-Objekt vom Downloader
            spider: Der Spider, der die Response verarbeiten wird
            
        Returns:
            None bei erfolgreicher Verarbeitung, oder Exception bei Fehler
        """
        return None

    def process_spider_output(self, response, result, spider):
        """
        Verarbeitet die vom Spider zurückgegebenen Items und Requests.
        
        Args:
            response: Das Response-Objekt, das vom Spider verarbeitet wurde
            result: Ein Iterable von Items/Requests vom Spider
            spider: Der Spider, der die Response verarbeitet hat
            
        Yields:
            Items oder Requests aus dem Spider-Result
        """
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        """
        Behandelt Exceptions, die im Spider auftreten.
        
        Args:
            response: Das Response-Objekt, bei dessen Verarbeitung die Exception auftrat
            exception: Die aufgetretene Exception
            spider: Der Spider, in dem die Exception auftrat
            
        Returns:
            None oder ein Iterable von Items/Requests
        """
        pass

    async def process_start(self, start):
        """
        Verarbeitet den Start-Request-Iterator des Spiders.
        
        Diese asynchrone Methode wird für jeden Request aus der
        Spider.start_requests()-Methode aufgerufen.
        
        Args:
            start: Async-Iterator über die Start-Requests des Spiders
            
        Yields:
            Items oder Requests aus dem Start-Iterator
        """
        async for item_or_request in start:
            yield item_or_request

    def spider_opened(self, spider):
        """
        Signal-Handler für das Öffnen eines Spiders.
        
        Args:
            spider: Der Spider, der geöffnet wurde
        """
        spider.logger.info("Spider opened: %s" % spider.name)


class ScrapeBibliothekenDownloaderMiddleware:
    """
    Downloader-Middleware für die Verarbeitung von HTTP-Requests und Responses.
    
    Diese Middleware wird zwischen dem Scrapy-Engine und dem Downloader ausgeführt.
    Sie kann verwendet werden für:
    - Modifikation von Request-Headern (z.B. User-Agent, Cookies)
    - Implementierung von Retry-Logik
    - Caching von Responses
    - Fehlerbehandlung bei Download-Problemen
    """
    
    @classmethod
    def from_crawler(cls, crawler):
        """
        Factory-Methode zum Erstellen der Middleware-Instanz.
        
        Args:
            crawler: Die Scrapy-Crawler-Instanz
            
        Returns:
            Eine neue Instanz der Middleware
        """
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        """
        Verarbeitet Requests, bevor sie vom Downloader heruntergeladen werden.
        
        Args:
            request: Das Request-Objekt, das verarbeitet werden soll
            spider: Der Spider, der den Request erstellt hat
            
        Returns:
            None: Request normal verarbeiten
            Response-Objekt: Request-Verarbeitung überspringen und Response zurückgeben
            Request-Objekt: Stattdessen diesen Request verarbeiten
            IgnoreRequest-Exception: Request überspringen
        """
        return None

    def process_response(self, request, response, spider):
        """
        Verarbeitet Responses vom Downloader, bevor sie an den Spider gehen.
        
        Args:
            request: Das ursprüngliche Request-Objekt
            response: Das Response-Objekt vom Downloader
            spider: Der Spider, für den die Response bestimmt ist
            
        Returns:
            Response-Objekt: Wird an Spider weitergeleitet
            Request-Objekt: Neuer Request wird verarbeitet statt Response
            IgnoreRequest-Exception: Response wird verworfen
        """
        return response

    def process_exception(self, request, exception, spider):
        """
        Behandelt Exceptions beim Download oder in process_request().
        
        Args:
            request: Das Request-Objekt, bei dem die Exception auftrat
            exception: Die aufgetretene Exception
            spider: Der Spider, für den der Request bestimmt war
            
        Returns:
            None: Exception-Verarbeitung fortsetzen
            Response-Objekt: Exception-Chain stoppen und Response zurückgeben
            Request-Objekt: Exception-Chain stoppen und Request verarbeiten
        """
        pass

    def spider_opened(self, spider):
        """
        Signal-Handler für das Öffnen eines Spiders.
        
        Args:
            spider: Der Spider, der geöffnet wurde
        """
        spider.logger.info("Spider opened: %s" % spider.name)

"""
Scrapy-Einstellungen für das Scrape-Bibliotheken-Projekt.

Diese Datei enthält die Hauptkonfiguration für das Scrapy-Projekt, einschließlich:
- Bot-Name und Spider-Module
- Crawling-Verhalten (Delays, Concurrency)
- Middleware- und Pipeline-Konfiguration
- User-Agent und robots.txt-Einstellungen

Wichtige Einstellungen:
- CONCURRENT_REQUESTS_PER_DOMAIN: Limitiert parallele Requests pro Domain
- DOWNLOAD_DELAY: Wartezeit zwischen Requests (höfliches Crawling)
- ROBOTSTXT_OBEY: Respektiert robots.txt der Zielseiten

Weitere Informationen:
https://docs.scrapy.org/en/latest/topics/settings.html
"""

# Scrapy settings for scrape_bibliotheken project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "scrape_bibliotheken"

SPIDER_MODULES = ["scrape_bibliotheken.spiders"]
NEWSPIDER_MODULE = "scrape_bibliotheken.spiders"

ADDONS = {}


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "scrape_bibliotheken (+http://www.yourdomain.com)"

# Obey robots.txt rules
# Hinweis: In den Spiders wird diese Einstellung teilweise überschrieben (ROBOTSTXT_OBEY = False)
# um alle relevanten Bibliotheksseiten crawlen zu können
ROBOTSTXT_OBEY = True

# Concurrency and throttling settings
# Limitierung auf 1 Request pro Domain zur gleichen Zeit, um Server nicht zu überlasten
#CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 1
# 1 Sekunde Wartezeit zwischen Requests für höfliches Crawling
DOWNLOAD_DELAY = 1

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "scrape_bibliotheken.middlewares.ScrapeBibliothekenSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "scrape_bibliotheken.middlewares.ScrapeBibliothekenDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "scrape_bibliotheken.pipelines.ScrapeBibliothekenPipeline": 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
# UTF-8-Encoding für exportierte Daten (JSON, CSV, etc.)
FEED_EXPORT_ENCODING = "utf-8"

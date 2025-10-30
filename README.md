# [WORK IN PRORESS] scrape_bibliotheken
Benutzt scrapy um Informationen über die Anmeldung von Bibliotheken zu sammeln

# Usage

## step 1

move to working dir then:

```
python -m scrapy crawl get_wikipedia -o bibliotheken.json
```

debug bibliotheken.json for missing urls

## step 2

```
python -m scrapy crawl keyword_spider -o urls.json
```

debug urls.json for missing urls

## step 3

push through AI to get relevant information with

```
python parse_with_ai.py
```

# [WORK IN PRORESS] scrape_bibliotheken
Benutzt scrapy um Informationen über die Anmeldung von Bibliotheken zu sammeln

# step 1 

move to working dir then:

```
python -m scrapy crawl BibliothekenSpider -o bibliotheken.json
```

# step 2

convert to markdown to debug pages

```
python json_to_markdown.py
```

# step 3

-> write spider to scrape possible pages with information
-> filter for keywords

import scrapy


class get_wikipedia(scrapy.Spider):
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
        # Hauptinhalt
        container = response.css("#mw-content-text > div.mw-content-ltr.mw-parser-output")

        for a in container.css("ul li a"):
            href = a.attrib.get("href")
            name = a.attrib.get("title")

            if not href:
                continue

            if href.startswith("/"):
                href = response.urljoin(href)

            # Filter für irrelevante Links
            if "action=edit" in href or "redlink=1" in href or "Liste" in href:
                continue

            # Folge dem Link zur Detailseite
            yield scrapy.Request(
                url=href,
                callback=self.parse_bibliothek,
                meta={"name": name, "wikipedia_url": href},
            )

    def parse_bibliothek(self, response):
        name = response.meta["name"]
        wikipedia_url = response.meta["wikipedia_url"]

        # Suche nach der Infobox (Vorlage_Infobox_Bibliothek)
        rows = response.css("#Vorlage_Infobox_Bibliothek > tbody > tr")

        website_url = None

        for row in rows:
            th_text = row.css("th::text").get()
            if th_text and "Website" in th_text:
                website_url = row.css("td a::attr(href)").get()
                break

        # relative URLs zu absoluten URLs umwandeln
        if website_url and website_url.startswith("/"):
            website_url = response.urljoin(website_url)

        yield {
            "name": name,
            "wikipedia_url": wikipedia_url,
            "website": website_url,
        }

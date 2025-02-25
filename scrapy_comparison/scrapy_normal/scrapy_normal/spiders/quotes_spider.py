import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/js/"]

    def parse(self, response):
        quotes = response.css("div.quote")
        if quotes:
            for quote in quotes:
                yield {
                    "text": quote.css("span.text::text").get(),
                    "author": quote.css("small.author::text").get(),
                }
        else:
            self.logger.info("クオートが見つかりませんでした。通常の Scrapy では JS がレンダリングされないためです。")

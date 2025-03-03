import scrapy
from scrapy_playwright.page import PageMethod  # 追加

class RealEstatePlaywrightSpider(scrapy.Spider):
    name = "realestate_playwright"
    allowed_domains = ["kzmlywhd669dcr21t5cl.lite.vusercontent.net"]
    start_urls = ["https://kzmlywhd669dcr21t5cl.lite.vusercontent.net/"]

    custom_settings = {
        "PLAYWRIGHT_BROWSER_TYPE": "chromium",
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, meta={
                "playwright": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", "div.property-card")
                ]
            })

    async def parse(self, response):
        properties = response.css("div.property-card")
        if properties:
            for prop in properties:
                yield {
                    "property_id": prop.attrib.get("data-property-id"),
                    "image_url": response.urljoin(prop.css("img.property-image::attr(src)").get()),
                    "title": prop.css("h3.property-title::text").get(),
                    "address": prop.css("p.property-address::text").get(),
                    "price": prop.css("span.property-price::text").get(),
                    "type": prop.css("span.property-type::text").get(),
                    "size": prop.css("div.property-size p::text").get(),
                    "layout": prop.css("div.property-layout p::text").get(),
                    "year": prop.css("div.property-year p::text").get(),
                    "station": prop.css("div.property-station p::text").get(),
                }
        else:
            self.logger.info("物件情報が見つかりませんでした。")

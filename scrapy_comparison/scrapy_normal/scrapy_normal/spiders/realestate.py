import scrapy

class RealEstateSpider(scrapy.Spider):
    name = "realestate"
    allowed_domains = ["kzmlywhd669dcr21t5cl.lite.vusercontent.net"]
    start_urls = ["https://kzmlywhd669dcr21t5cl.lite.vusercontent.net/"]

    def parse(self, response):
        # 物件カードの要素を取得
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
            self.logger.info("物件情報が見つかりませんでした。JSレンダリングが必要な場合は、Splashなどのツールをご検討ください。")

import scrapy

class SpaceMarketSpider(scrapy.Spider):
    name = "spacemarket"
    allowed_domains = ["spacemarket.com"]
    start_urls = ["https://www.spacemarket.com/lists/r9kf8h06urts2mv0s0w5sg11/"]

    def parse(self, response):
        self.logger.info("Response status: %s", response.status)
        # まずはレスポンスの HTML の一部をログに出力して内容を確認
        self.logger.debug("Response HTML snippet: %s", response.text[:1000])
        
        # CSS セレクタで各スペースのブロックを取得
        listings = response.css("li.css-1qog96z")
        self.logger.info("Found %d listings", len(listings))
        for listing in listings:
            title = listing.css("a.css-pvls0p::text").get()
            subtitle = listing.css("p.css-1hhxm3a::text").get()
            price = listing.css("div.css-mijawg em.css-axej1t::text").get()
            review_score = listing.css("span.css-1lzfy2k::text").get()
            review_count_raw = listing.css("span.css-1t0mqy6::text").get()
            review_count = review_count_raw.strip("（）") if review_count_raw else None
            location = listing.css("div.css-1ihb5gf ul.css-1pj0ozd li:nth-child(2) span.css-j6x3og::text").get()
            
            yield {
                "title": title,
                "subtitle": subtitle,
                "price": price,
                "location": location,
                "review_score": review_score,
                "review_count": review_count,
            }

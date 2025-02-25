import scrapy

class SpaceMarketSpider(scrapy.Spider):
    name = "spacemarket"
    allowed_domains = ["spacemarket.com"]
    start_urls = ["https://www.spacemarket.com/lists/r9kf8h06urts2mv0s0w5sg11/"]

    custom_settings = {
        # Playwright の設定（既にプロジェクトの settings で定義している場合は不要）
        "PLAYWRIGHT_BROWSER_TYPE": "chromium",
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        # robots.txt の制約を解除（必要に応じて）
        "ROBOTSTXT_OBEY": False,
    }

    def start_requests(self):
        for url in self.start_urls:
            # ページ内のスペースリストが表示されるまで待機
            yield scrapy.Request(url, meta={
                "playwright": True,
                "playwright_page_methods": [
                    {"method": "wait_for_selector", "args": ["li.css-1qog96z"]}
                ]
            })

    def parse(self, response):
        # 各スペースのリスト要素
        listings = response.css("li.css-1qog96z")
        for listing in listings:
            title = listing.css("a.css-pvls0p::text").get()
            subtitle = listing.css("p.css-1hhxm3a::text").get()
            price = listing.css("div.css-mijawg em.css-axej1t::text").get()
            review_score = listing.css("span.css-1lzfy2k::text").get()
            review_count_raw = listing.css("span.css-1t0mqy6::text").get()
            review_count = review_count_raw.strip("（）") if review_count_raw else None
            # 場所は、ul 内の2番目の li のテキストを取得（例：新宿駅 徒歩1分）
            location = listing.css("div.css-1ihb5gf ul.css-1pj0ozd li:nth-child(2) span.css-j6x3og::text").get()
            
            yield {
                "title": title,
                "subtitle": subtitle,
                "price": price,
                "location": location,
                "review_score": review_score,
                "review_count": review_count,
            }

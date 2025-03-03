import scrapy

# もし scrapy_playwright.page_methods モジュールが存在しない場合は、下記のようにフォールバック定義する
try:
    from scrapy_playwright.page_methods import PageMethod
except ImportError:
    class PageMethod:
        def __init__(self, method, *args, **kwargs):
            self.method = method
            self.args = args
            self.kwargs = kwargs
        def __repr__(self):
            return f"PageMethod({self.method!r}, args={self.args}, kwargs={self.kwargs})"

class InstabaseRentalspaceSpider(scrapy.Spider):
    name = "instabase_rentalspace"
    allowed_domains = ["instabase.jp"]
    start_urls = ["https://www.instabase.jp/rentalspace"]

    custom_settings = {
        "PLAYWRIGHT_BROWSER_TYPE": "chromium",
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        # Instabase 側は自動アクセスを拒否する場合があるため、robots.txt の制約は無視
        "ROBOTSTXT_OBEY": False,
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,
                    # PageMethod オブジェクトを使用して対象要素が表示されるまで待機
                    "playwright_page_methods": [
                        PageMethod("wait_for_selector", "li.w-full.grow.border-border-medium-emphasis")
                    ]
                }
            )

    def parse(self, response):
        # 各レンタルスペースのブロック（リスト要素）
        listings = response.css("li.w-full.grow.border-border-medium-emphasis")
        for listing in listings:
            # タイトル（大見出しのテキスト）
            title = listing.css("div.col-start-6.col-end-13.mt-4.lg\\:mt-0 p.mt-2::text").get()
            if title:
                title = title.strip()
            # サブタイトル：一覧上部のステータス情報（例：「新着」「今すぐ予約可能」など）を結合
            subtitle_list = listing.css("div.col-start-6.col-end-13.mt-4.lg\\:mt-0 div.flex.flex-wrap.gap-2 span::text").getall()
            subtitle = ", ".join(s.strip() for s in subtitle_list if s.strip())
            # 価格：mdl:hidden 内の価格部分
            price = listing.css("div.mt-1.flex.flex-col.mdl\\:hidden div.flex.justify-end p.flex.flex-nowrap.items-end span.text-4xl::text").get()
            if price:
                price = price.strip()
                if not price.startswith("￥"):
                    price = "￥" + price
            # 場所：p.mt-1.flex.gap-1 内のテキスト（アイコンを除く）
            location_parts = listing.css("div.col-start-6.col-end-13.mt-4.lg\\:mt-0 p.mt-1.flex.gap-1 span::text").getall()
            location = " ".join(part.strip() for part in location_parts if part.strip())
            # レビュー点数とレビュー数：mdl:grid 内の要素
            review_score = listing.css(
                "div.col-start-6.col-end-13.mt-4.lg\\:mt-0 div.hidden.grid-flow-col.justify-between.mdl\\:grid p.inline-grid.grid-flow-col.items-start span.text-sm.font-semibold.text-secondary::text"
            ).get()
            review_count_raw = listing.css(
                "div.col-start-6.col-end-13.mt-4.lg\\:mt-0 div.hidden.grid-flow-col.justify-between.mdl\\:grid p.inline-grid.grid-flow-col.items-start span.whitespace-nowrap.text-sm.font-light.leading-5.text-text-high-emphasis::text"
            ).get()
            if review_count_raw:
                review_count = review_count_raw.strip("（）").replace("件", "").strip()
            else:
                review_count = ""
            
            yield {
                "title": title,
                "subtitle": subtitle,
                "price": price,
                "location": location,
                "review_score": review_score,
                "review_count": review_count,
            }

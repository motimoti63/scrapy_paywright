import os

project_structure = {
    # 通常の Scrapy プロジェクト
    "scrapy_comparison/scrapy_normal/scrapy.cfg": """[settings]
default = scrapy_normal.settings
""",
    "scrapy_comparison/scrapy_normal/scrapy_normal/__init__.py": "",
    "scrapy_comparison/scrapy_normal/scrapy_normal/items.py": """import scrapy

class ScrapyComparisonItem(scrapy.Item):
    pass
""",
    "scrapy_comparison/scrapy_normal/scrapy_normal/middlewares.py": """# scrapy_normal 用のミドルウェア設定（必要に応じて編集）
""",
    "scrapy_comparison/scrapy_normal/scrapy_normal/pipelines.py": """# scrapy_normal 用のパイプライン設定（必要に応じて編集）
""",
    "scrapy_comparison/scrapy_normal/scrapy_normal/settings.py": """BOT_NAME = "scrapy_normal"

SPIDER_MODULES = ["scrapy_normal.spiders"]
NEWSPIDER_MODULE = "scrapy_normal.spiders"

# robots.txt を遵守
ROBOTSTXT_OBEY = True
""",
    "scrapy_comparison/scrapy_normal/scrapy_normal/spiders/__init__.py": "",
    "scrapy_comparison/scrapy_normal/scrapy_normal/spiders/quotes_spider.py": """import scrapy

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
""",
    # Scrapy-Playwright プロジェクト
    "scrapy_comparison/scrapy_playwright/scrapy.cfg": """[settings]
default = scrapy_playwright.settings
""",
    "scrapy_comparison/scrapy_playwright/scrapy_playwright/__init__.py": "",
    "scrapy_comparison/scrapy_playwright/scrapy_playwright/items.py": """import scrapy

class ScrapyComparisonItem(scrapy.Item):
    pass
""",
    "scrapy_comparison/scrapy_playwright/scrapy_playwright/middlewares.py": """# scrapy_playwright 用のミドルウェア設定（必要に応じて編集）
""",
    "scrapy_comparison/scrapy_playwright/scrapy_playwright/pipelines.py": """# scrapy_playwright 用のパイプライン設定（必要に応じて編集）
""",
    "scrapy_comparison/scrapy_playwright/scrapy_playwright/settings.py": """BOT_NAME = "scrapy_playwright"

SPIDER_MODULES = ["scrapy_playwright.spiders"]
NEWSPIDER_MODULE = "scrapy_playwright.spiders"

# robots.txt を遵守
ROBOTSTXT_OBEY = True

# Scrapy-Playwright の設定
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

PLAYWRIGHT_BROWSER_TYPE = "chromium"
""",
    "scrapy_comparison/scrapy_playwright/scrapy_playwright/spiders/__init__.py": "",
    "scrapy_comparison/scrapy_playwright/scrapy_playwright/spiders/quotes_playwright_spider.py": """import scrapy

class QuotesPlaywrightSpider(scrapy.Spider):
    name = "quotes_playwright"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/js/"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, meta={
                "playwright": True,
                "playwright_page_methods": [
                    {"method": "wait_for_selector", "args": ["div.quote"]}
                ]
            })

    async def parse(self, response):
        quotes = response.css("div.quote")
        for quote in quotes:
            yield {
                "text": quote.css("span.text::text").get(),
                "author": quote.css("small.author::text").get(),
            }
"""
}

def create_project(structure):
    for path, content in structure.items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    print("プロジェクト構成が正常に作成されました。")

if __name__ == "__main__":
    create_project(project_structure)

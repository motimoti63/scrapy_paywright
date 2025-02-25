BOT_NAME = "playwright_project"

SPIDER_MODULES = ["playwright_project.spiders"]
NEWSPIDER_MODULE = "playwright_project.spiders"

# robots.txt を遵守
ROBOTSTXT_OBEY = True

# Scrapy‑Playwright の設定（正しいモジュールパス）
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

PLAYWRIGHT_BROWSER_TYPE = "chromium"

# FEEDS = {
#     'quotes.csv': {
#         'format': 'csv',
#         'fields': ['text', 'author'],  # 出力したいカラムを指定
#     },
# }

FEED_EXPORT_ENCODING = "utf-8"
FEED_EXPORT_INDENT = 4

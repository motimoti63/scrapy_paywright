BOT_NAME = "scrapy_playwright"

SPIDER_MODULES = ["scrapy_playwright.spiders"]
NEWSPIDER_MODULE = "scrapy_playwright.spiders"

# robots.txt を遵守
ROBOTSTXT_OBEY = True

# Scrapy‑Playwright の設定
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.downloadhandler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.downloadhandler.ScrapyPlaywrightDownloadHandler",
}
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

PLAYWRIGHT_BROWSER_TYPE = "chromium"

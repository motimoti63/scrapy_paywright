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

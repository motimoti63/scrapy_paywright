BOT_NAME = "playwright_project"

SPIDER_MODULES = ["playwright_project.spiders"]
NEWSPIDER_MODULE = "playwright_project.spiders"

# robots.txt はグローバルには遵守しますが、必要に応じて各スパイダーで上書き可能
# ROBOTSTXT_OBEY = True

# Scrapy‑Playwright の設定（正しいモジュールパス）
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

# PLAYWRIGHT_BROWSER_TYPE = "chromium"

# ブラウザからのアクセスに近づけるためのヘッダー設定
DEFAULT_REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "ja,en;q=0.9",
}

FEED_EXPORT_ENCODING = "utf-8"
FEED_EXPORT_INDENT = 4

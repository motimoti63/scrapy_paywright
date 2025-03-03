BOT_NAME = "scrapy_normal"

SPIDER_MODULES = ["scrapy_normal.spiders"]
NEWSPIDER_MODULE = "scrapy_normal.spiders"

# robots.txt を遵守
ROBOTSTXT_OBEY = True

# ブラウザからのアクセスに近づけるためのヘッダー設定
DEFAULT_REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "ja,en;q=0.9",
}
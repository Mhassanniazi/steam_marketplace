import scrapy
from scrapy.crawler import CrawlerProcess
import json
import math
import re

class SteamMarketplace(scrapy.Spider):
    name = "steam_marketplace"

    URL = "https://steamcommunity.com/market/search/render/?query={}&start={}&count={}&search_descriptions={}&sort_column={}&sort_dir={}&norender={}"
    PARAMS = {
        "query": "",
        "start": 0,                # OFFSET
        "count": 100,              # LIMIT
        "search_descriptions": 0,
        "sort_column": "popular",
        "sort_dir": "desc",
        "norender": 1
    }
    # within-script-configuration
    custom_settings = {
        "USER_AGENT" : "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
        "DOWNLOAD_DELAY": 0.2,
        "COOKIES_ENABLED": False,
        "CONCURRENT_REQUESTS": 1,

        "ITEM_PIPELINES": {
            "pipelines.SteamMarketplacePipeline": 300
        },

        # # rotating-proxies-configuration
        # "ROTATING_PROXY_LIST" : ["108.59.14.208:13040", "108.59.14.203:13040"],
        # "DOWNLOADER_MIDDLEWARES" : {
        #     "rotating_proxies.middlewares.RotatingProxyMiddleware" : 610,
        #     "rotating_proxies.middlewares.BanDetectionMiddleware" : 620
        # }
    }

    def start_requests(self):
        url = self.URL.format(
            self.PARAMS['query'],
            self.PARAMS['start'],
            self.PARAMS['count'],
            self.PARAMS['search_descriptions'],
            self.PARAMS['sort_column'],
            self.PARAMS['sort_dir'],
            self.PARAMS['norender']
        )
        yield scrapy.Request(url=url, callback=self.parse, meta={"InitialRequest": True})
    
    def parse(self, response):
        parsed_data = json.loads(response.text)
        results = parsed_data.get("results")

        for result in results:
            description_raw = " ".join([item.get('value',"").strip() for item in (result.get('asset_description').get('descriptions') or [])],)
            description = re.sub(r"\s+", " ", description_raw)
            data = {
                "Game": result.get("app_name"),
                "Item": result.get("name"),
                "Type": result.get("asset_description").get("type"),
                "Listings": result.get("sell_listings"),
                "Price": result.get("sell_price_text"),
                "Description": description.strip(),
                "Icon": result.get("app_icon"),
                "Product URL": f"https://steamcommunity.com/market/listings/{result.get('asset_description').get('appid')}/{result.get('hash_name')}"
            }
            yield data

        if response.meta.get("InitialRequest"):
            # ∴ total records / records per page => 492109/100 = ... pages 
            pages = math.ceil(int(parsed_data.get("total_count"))/self.PARAMS['count'])
            for i in range(1, pages):
                yield scrapy.Request(
                    self.URL.format(
                        self.PARAMS['query'],
                        i*self.PARAMS['count'],
                        self.PARAMS['count'],
                        self.PARAMS['search_descriptions'],
                        self.PARAMS['sort_column'],
                        self.PARAMS['sort_dir'],
                        self.PARAMS['norender']
                    ),
                    callback=self.parse
                )
        
process = CrawlerProcess()
process.crawl(SteamMarketplace)
process.start()
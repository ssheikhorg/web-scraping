from typing import Any

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor



class AdidasSpider(CrawlSpider):
    name = "adidas"
    allowed_domains = ["shop.adidas.jp"]
    start_urls = ["https://shop.adidas.jp/"]

    # https://shop.adidas.jp/men/
    # https://shop.adidas.jp/item/?cat2Id=marimekko23ss&gender=mens&order=1
    # https://shop.adidas.jp/products/HR3028/

    # """parse data from product page while mounting from men to item"""
    rules = (
        Rule(LinkExtractor(allow="men")),
        Rule(LinkExtractor(allow="item")),
        Rule(LinkExtractor(allow="products"), callback="parse_product"),
    )

    def parse_product(self, response: Any) -> Any:
        """parse product page"""
        yield {
            "name": response.css("h1::text").get(),
            "price": response.css(".price::text").get(),
            "description": response.css(".description::text").get(),
            "url": response.url,
        }

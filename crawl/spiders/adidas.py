from typing import Any

import scrapy
from scrapy.http import HtmlResponse
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

    def parse_product(self, response: HtmlResponse) -> dict[str, Any]:
        """parse product page"""
        # parse only 5 items
        if self.crawler.stats.get_value("downloader/response_count") > 5:
            self.crawler.engine.close_spider(self, "crawled enough items")

        yield {
            "breadcrumb_category": response.css(".breadcrumbListItemLink::text").getall(),
            "category": f'{response.css(".test-genderName::text").get()} {response.css(".test-categoryName::text").get()}',
            "product_name": response.css('.test-itemTitle::text').get(),
            "price": response.css(".test-price-value::text").get(),
            "image_url": response.css(".test-slider-list img::attr(src)").getall(),
            "coordinated_product_name": response.css(".test-coordinated-itemTitle::text").getall(),
            "coordinated_price": response.css(".test-price-value::text").get(),
        }

from typing import Any

from scrapy.http import HtmlResponse
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class AdidasSpider(CrawlSpider):
    name = "adidas"
    allowed_domains = ["shop.adidas.jp"]
    start_urls = ["https://shop.adidas.jp/"]

    # """parse data from product page while mounting from men to item"""
    rules = (
        Rule(LinkExtractor(allow="men")),
        Rule(LinkExtractor(allow="item")),
        Rule(LinkExtractor(allow="products"), callback="parse_product"),
    )

    def parse_product(self, response: HtmlResponse) -> dict[str, Any]:
        """parse product page"""
        if self.crawler.stats.get_value("downloader/response_count") > 300:
            self.crawler.engine.close_spider(self, "crawled enough items")

        yield {
            "breadcrumb_category": response.css(".breadcrumbListItemLink::text").getall(),
            "category": f'{response.css(".test-genderName::text").get()} {response.css(".test-categoryName::text").get()}',
            "product_name": response.css('.test-itemTitle::text').get(),
            "pricing": response.css(".test-price-value::text").get(),
            "image_urls": ", ".join(
                ["https://shop.adidas.jp" + url for url in response.css('.main_image::attr(src)').getall()]),
            "descriptions_title": response.css('.test-commentItem-subheading::text').get(),
            "descriptions": response.css('.test-commentItem-mainText::text').get(),
            "description_itemized": response.css('.test-feature::text').getall(),
            "sizes": response.css("ul.sizeSelectorList > li > button::text").getall(),
            "tags": response.css(".itemTagsPosition > div > div > a::text").getall()
        }

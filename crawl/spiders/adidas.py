import scrapy


class AdidasSpider(scrapy.Spider):
    name = "adidas"
    allowed_domains = ["shop.adidas.jp"]
    start_urls = ["http://shop.adidas.jp/"]

    def parse(self, response):
        pass

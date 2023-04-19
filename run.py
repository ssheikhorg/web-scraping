from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from crawl.spiders.adidas import AdidasSpider

process = CrawlerProcess(get_project_settings())
process.crawl(AdidasSpider)
process.start()

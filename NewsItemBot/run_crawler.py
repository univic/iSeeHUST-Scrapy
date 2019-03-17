
from scrapy.crawler import CrawlerProcess
from NewsItemBot.spiders import husteco_spider
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())
process.crawl(husteco_spider.HustecoSpider)
process.start()

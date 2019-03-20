import os
from scrapy import cmdline
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from NewsItemBot.NewsItemBot import settings
from NewsItemBot.NewsItemBot.spiders import husteco_spider

import logging


sLogger = logging.getLogger(__name__)


def run_all_crawler():
    print(f"Subprocess {__name__} running, PID {os.getpid()}")
    cmdline.execute(["scrapy", "crawlall"])
    """
    process = CrawlerProcess(get_project_settings())
    process.crawl(husteco_spider.HustecoSpider)
    process.start()
    """


# 运行爬虫
def run_crawler_aux():
    print(f"Subprocess {__name__} running, PID {os.getpid()}")
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(husteco_spider.HustecoSpider)
    process.start()

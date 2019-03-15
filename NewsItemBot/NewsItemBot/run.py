
from scrapy.crawler import CrawlerProcess
from spiders.hustcm_spider import HustcmSpider

process = CrawlerProcess({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586'
})

process.crawl(HustcmSpider)
process.start()

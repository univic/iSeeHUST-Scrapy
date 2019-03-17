import iSeeHUST.iSeeHUST_main
from scrapy.crawler import CrawlerProcess
from NewsItemBot.NewsItemBot.spiders import husteco_spider
import logging
from logging import handlers
import os
from scrapy.utils.project import get_project_settings
from NewsItemBot.NewsItemBot import settings as bot_settings
from scrapy.settings import Settings

try:
    import iSeeHUST.WebMonConfig_deploy_env as WebMonPara
except ImportError as e:
    import iSeeHUST.WebMonConfig as WebMonPara


def create_logger(log_file='NAV'):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    log_file_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'tmp', str(log_file) + '.log')
    handler = handlers.RotatingFileHandler(log_file_path, mode='a',
                                           maxBytes=WebMonPara.APP_CONFIG['MAX_LOG_SIZE'] * 1024 * 1024,
                                           backupCount=1, encoding=None,)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s:%(lineno)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


sLogger = create_logger('NAV')

# 运行爬虫
os.chdir("NewsItemBot")
process = CrawlerProcess(get_project_settings())
process.crawl(husteco_spider.HustecoSpider)
process.start()

# iSeeHUST.iSeeHUST_main.app.run(host='0.0.0.0', port=1037, debug=True, threaded=True)
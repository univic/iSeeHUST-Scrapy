import os
import time
import datetime
from multiprocessing import Process
from scrapy import cmdline
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from NewsItemBot.NewsItemBot import settings
from NewsItemBot.NewsItemBot.spiders import husteco_spider
from iSeeHUST import DB
from conf.configs import CONFIGS

import logging


sLogger = logging.getLogger(__name__)

# 连接数据库
dba = DB.DBConn()


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


# 定时运行爬虫
def crawler_dispatcher():
    t_next_run = ''
    while True:
        t_next_run_delta, t_next_run = next_run_time(t_next_run)
        dba.db["crawler_status"].update(
            {"name": "crawler_run_time"},
            {"$set": {"value": datetime.datetime.now()}}, upsert=True)
        p3 = Process(target=run_all_crawler)
        p3.start()
        print('sleeping, next run at', t_next_run)
        time.sleep(t_next_run_delta)


# 计算下次爬虫运行时间
def next_run_time(t_next_run):
    is_night = False
    is_weekend = False
    t_now = datetime.datetime.now()

    # if t_next_run does not exist, reckon it as first run
    if t_next_run == '':
        t_next_run_delta = (59 - t_now.minute) * 60 + (60 - t_now.second)
        if t_next_run_delta < CONFIGS['APP_CONFIGS']['SAFE_CRAWL_INTERVAL'] * 60:
            t_next_run_delta = (59 - t_now.minute) * 60 * 2 + (60 - t_now.second)
        t_next_run = t_now + datetime.timedelta(seconds=t_next_run_delta)
    else:
        # is it now weekend and/or night in China
        if t_now.weekday() == 5 or t_now.weekday() == 6:
            is_weekend = True
        if not CONFIGS['APP_CONFIGS']['SHIFT_START'] <= t_now.hour <= CONFIGS['APP_CONFIGS']['SHIFT_END']:
            is_night = True

        # Calculate time interval
        if CONFIGS['APP_CONFIGS']['WEEKEND_SHIFT'] and is_weekend:
            if CONFIGS['APP_CONFIGS']['NIGHT_SHIFT'] and is_night:
                sLogger.info('In weekend&night mode')
                t_next_run_delta = CONFIGS['APP_CONFIGS']['OFFSHIFT_INTERVAL'] * 2 * 60
            else:
                sLogger.info('In weekend mode')
                t_next_run_delta = CONFIGS['APP_CONFIGS']['OFFSHIFT_INTERVAL'] * 60
        elif CONFIGS['APP_CONFIGS']['NIGHT_SHIFT'] and is_night:
            sLogger.info('In night mode')
            t_next_run_delta = CONFIGS['APP_CONFIGS']['OFFSHIFT_INTERVAL'] * 60
        else:
            t_next_run_delta = CONFIGS['APP_CONFIGS']['FETCH_INTERVAL'] * 60
        t_next_run = t_next_run + datetime.timedelta(seconds=t_next_run_delta)
    print(type(t_next_run))

    dba.db["crawler_status"].update(
        {
            "name": "next_run_time"},
        {"$set": {"value": t_next_run}
        }, upsert=True)

    return t_next_run_delta, t_next_run

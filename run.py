# /usr/bin/env python3
# -*- coding: utf-8 -*-
# Author : univic

import os
import logging
from logging import handlers
from multiprocessing import Process
from NewsItemBot import run_crawler
import iSeeHUST.iSeeHUST_main
from conf.configs import CONFIGS


def create_logger(log_file='iSeeHUST'):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    log_file_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'tmp', str(log_file) + '.log')
    handler = handlers.RotatingFileHandler(log_file_path, mode='a',
                                           maxBytes=CONFIGS['APP_CONFIGS']['MAX_LOG_SIZE'] * 1024 * 1024,
                                           backupCount=1, encoding=None, )
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s:%(lineno)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


sLogger = create_logger('iSeeHUST')


# 进行爬虫运行的时间调度
def crawler_dispatcher():
    # 调用commands模块命令，运行全部爬虫
    run_crawler.crawler_dispatcher()


# 运行web服务
def run_web_server():
    # TODO 整合HTML模板
    iSeeHUST.iSeeHUST_main.app.run(host='0.0.0.0', port=1037, debug=False, threaded=True, use_reloader=False)


if __name__ == "__main__":

    sLogger.info(f"Main process running, PID {os.getpid()}")

    # 通过多进程方式启动爬虫服务和网页服务
    # p1 = Process(target=run_crawler_aux)
    p1 = Process(target=crawler_dispatcher)
    p2 = Process(target=run_web_server)
    p1.start()
    p2.start()
    sLogger.info(f"Subprocess NewsItemBot running, PID {p1.pid}")
    sLogger.info(f"Subprocess iSeeHUST running, PID {p2.pid}")

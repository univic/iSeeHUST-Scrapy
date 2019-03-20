# /usr/bin/env python3
# -*- coding: utf-8 -*-
# Author : univic

import os
import logging
from logging import handlers
import multiprocessing
from multiprocessing import Process
from NewsItemBot import run_crawler

import iSeeHUST.iSeeHUST_main


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


# 进行爬虫运行的时间调度
def crawler_dispatch():
    # TODO 进行爬虫运行的时间调度
    # 调用commands模块命令，运行全部爬虫
    run_crawler.run_all_crawler()


# 运行web服务
def run_web_server():
    # TODO 整合HTML模板
    iSeeHUST.iSeeHUST_main.app.run(host='0.0.0.0', port=1037, debug=True, threaded=True)


if __name__ == "__main__":

    print("Main process running, PID ", os.getpid())

    # 切换至爬虫主目录——Scrapy根据当前路径查找cfg文件
    main_project_path = os.path.abspath(os.getcwd())
    bot_project_path = os.path.join(main_project_path, "NewsItemBot")
    os.chdir(bot_project_path)
    print("Working directory changed to ", bot_project_path)

    # 通过多进程方式启动爬虫服务和网页服务
    # p1 = Process(target=run_crawler_aux)
    p1 = Process(target=crawler_dispatch)
    p2 = Process(target=run_web_server)
    p1.start()
    p2.start()
    print(f"Subprocess NewsItemBot running, PID {p1.pid}")
    print(f"Subprocess iSeeHUST running, PID {p2.pid}")


# /usr/bin/env python3
# -*- coding: utf-8 -*-
# Author : univic

import re
import pymongo
import logging
import datetime


def get_logger():
    logger = logging.getLogger(__name__)
    return logger


sLogger = get_logger()


class TextReplyDispatch(object):
    def __init__(self, content):
        self.content = content

        # 关键词和对应的处理方法
        self.keyword_dict = {
            "新消息": self.get_recent_news_item
        }

        db_client = pymongo.MongoClient()
        active_db = db_client['iSeeHUST']
        self.rec_col = active_db['record_items']

    def reply_dispatch(self):
        return_result = self.pattern_recog(self.content)
        return return_result

    def pattern_recog(self, content):

        # 进行传送门的模式识别
        p = re.compile(r'^[0-9]{2,4}$')  # 传送门数字pattern
        match = re.match(p, str(content))
        if match:
            sLogger.info(f"WARP GATE RX: {content}")
            return_str = self.warp_gate_handle(content)

        # 如不符合，检查是否为keyword_dict中已有的关键词，并调用对应方法
        elif content in self.keyword_dict:
            sLogger.info(f"KEYWORD RX: {content}")
            return_str = self.keyword_dict[content]()

        else:
            sLogger.info("UNMATCHED CONTENT", content)
            return_str = ""
        return return_str

    @staticmethod
    def warp_gate_handle(entry_id):

        # 连接数据库
        db_client = pymongo.MongoClient()
        active_db = db_client['iSeeHUST']
        rec_col = active_db['record_items']

        # 查找对应传送门编号
        r = rec_col.find({"serial_id": entry_id})
        if r.count() > 0:
            if r.count() == 1:
                item = r[0]
                return_str = f'[传送门{item["serial_id"]}]<a href={item["href"]}>{item["title"]}</a>'
                sLogger.info(f'WARP GATE {item["serial_id"]} FOUNDED')
            else:
                sLogger.warning(f'REDUNDANT WARP GATE ENTRY {entry_id}')
                return_str = None
        else:
            sLogger.info(f'WARP GATE {entry_id} NOT FOUND')
            return_str = u'传送门不存在'

        return return_str

    def get_recent_news_item(self):
        query_date_limiter = datetime.datetime.now() - datetime.timedelta(days=1)
        query_date_limiter.replace(hour=0, minute=0, second=0)
        r = self.rec_col.find({"item_date": {"$gt": query_date_limiter}})
        return_str = ""
        if r.count() == 0:
            return_str = "今日暂无新消息"
        else:
            for item in r:
                return_str += f'[{item["serial_id"]}]<a href={item["href"]}>{item["title"]}</a>\n'
        return return_str



if __name__ == "__main__":
    list = [30, 88, 29, 28]
    for id in list:
        T = TextReplyDispatch(id)
        a, b = T.reply_dispatch()
        print(a, b)

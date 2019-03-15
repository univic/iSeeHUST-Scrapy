# /usr/bin/env python3
# -*- coding: utf-8 -*-
# Author : univic

import re
import pymongo
import logging


def get_logger():
    logger = logging.getLogger('iSeeHUST.WeChatReply')
    return logger


sLogger = get_logger()


class TextReplyDispatch(object):
    def __init__(self, content):
        self.flag_must_reply = False
        self.content = content

    def reply_dispatch(self):
        return_result = self.pattern_recog(self.content)
        return return_result, self.flag_must_reply

    def pattern_recog(self, content):
        return_str = None

        # 模式识别-传送门
        p1 = re.compile(r'^[0-9]{2,4}$')  # 传送门数字pattern
        match = re.match(p1, str(content))
        if match:
            sLogger.info("WARP GATE RX: %s" % content)
            self.flag_must_reply = True
            return_str = self.warp_gate_handle(content)

        else:
            sLogger.info("UNMATCHED CONTENT", content)
            return_str = ""
        return return_str

    def warp_gate_handle(self, entry_id):

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


if __name__ == "__main__":
    list = [30, 88, 29, 28]
    for id in list:
        T = TextReplyDispatch(id)
        a, b = T.reply_dispatch()
        print(a, b)

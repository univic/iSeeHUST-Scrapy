# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# from scrapy import exceptions
import logging
import bson
from scrapy.mail import MailSender
import iSeeHUST.DB

logger = logging.getLogger(__name__)


class NewsitembotPipeline(object):

    def __init__(self):
        # 创建数据库连接
        logger.info('Pipeline running')
        print('Pipeline running')
        self.db = iSeeHUST.DB.DBConn()

    # 为自增字段查询并更新最新值
    def get_next_sequence(self, key_name):
        ret = self.db.db["counters"].find_and_modify({"name": key_name},
                                                     {"$inc": {"seq": bson.Int64(1)}},
                                                     safe=True,
                                                     new=True)
        return ret["seq"]

    # 提取标签信息
    def process_tags(self):
        pass

    def process_item(self, item, spider):
        data = dict(item)

        # 查询某链接是否已经在数据集中存在,如存在则不写入
        if self.db.record_items_col.count({"href": data["href"]}) == 0:
            logger.debug(">>>>>>>inserting item")
            # 调用get_next_sequence函数获取并更新自增字段最新值
            data["serial_id"] = self.get_next_sequence("serial_id")
            self.db.record_items_col.insert(data)
        else:
            logger.debug(f">>>>>>>dumping item {data}")
        return item

        # raise exceptions.DropItem


class EMailPipeline(object):
    mailer = MailSender()
    mailer.send(to=["xyzhgwf@hotmail.com"], subject="This is a test", body="Test body")

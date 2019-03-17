import pymongo
from pymongo import errors
import logging
import bson
# import traceback
try:
    import iSeeHUST.WebMonConfig_deploy_env as WebMonPara
except ImportError as e:
    import iSeeHUST.WebMonConfig as WebMonPara


def get_logger():
    logger = logging.getLogger(__name__)
    return logger


sLogger = get_logger()


class DBConn(object):

    def __init__(self):
        try:
            self.db_msg = None
            # 连接MongoDB数据库
            self.client = pymongo.MongoClient(host=WebMonPara.DB_CONFIGS["host"],
                                              port=WebMonPara.DB_CONFIGS["port"]
                                              )
            self.db = self.client[WebMonPara.DB_CONFIGS["database"]]
            self.record_items_col = self.db["record_items"]

            # 是否需要鉴权
            if WebMonPara.DB_CONFIGS["authenticate"]:
                self.db.authenticate(WebMonPara.DB_CONFIGS['username'], WebMonPara.DB_CONFIGS['password'])

            # 如数据库不存在，或counters数据集不存在，则进行初始化
            if WebMonPara.DB_CONFIGS["database"] not in self.client.list_database_names():
                self.db_init()
            elif "counters" not in self.db.list_collection_names():
                self.db_init()

        except pymongo.errors.ServerSelectionTimeoutError as e:
            self.db_msg = e
            sLogger.error(e)

    # 初始化数据库，初始化计数器数据集
    def db_init(self):
        col = self.db["counters"]
        col.insert_one({
            "name": "serial_id",
            "seq": bson.Int64(100)
        }
        )

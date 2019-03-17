import pymongo
import iSeeHUST.WebMonPara as Para
import logging
import bson


def get_logger():
    logger = logging.getLogger(__name__)
    return logger


sLogger = get_logger()


class DBObject(object):

    def __init__(self):
        try:
            self.client = pymongo.MongoClient(host=Para.DB_CONFIGS["host"],
                                              port=Para.DB_CONFIGS["port"]
                                              )
            self.db = self.client.Para.DB_CONFIGS["database"]
            self.record_items_col = self.db["record_items"]

            if Para.DB_CONFIGS["authenticate"]:
                self.db.authenticate(Para.DB_CONFIGS['username'], Para.DB_CONFIGS['password'])

            if Para.DB_CONFIGS["database"] not in self.client.list_database_names():
                self.db_init()
            elif "counters" not in self.db.list_collection_names():
                self.db_init()

        except Exception as e:
            pass

    def db_init(self):
        col = self.db["counters"]
        col.insert_one({
            "name": "serial_id",
            "seq": bson.Int64(100)
        }
        )

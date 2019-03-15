import pymongo
import datetime

dtn = datetime.datetime.now()

db_client = pymongo.MongoClient()
active_db = db_client['iSeeHUST']
rec_col = active_db['record_items']

query_date_limiter = datetime.datetime.now() - datetime.timedelta(days=15)
query_date_limiter.replace(hour=0, minute=0, second=0)
r = rec_col.find({"serial_id": 30})

print(r.count())
item = r[0]
return_str = f'[传送门{item["serial_id"]}]<a href={item["href"]}>{item["title"]}</a>'
print(return_str)



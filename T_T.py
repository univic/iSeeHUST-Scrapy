import iSeeHUST.iSeeHUST_main as m

m.app.run(host='0.0.0.0', port=1037, debug=True, threaded=True)








"""
dtn = datetime.datetime.now()

db = DB.DBConn()

query_date_limiter = datetime.datetime.now() - datetime.timedelta(days=15)
query_date_limiter.replace(hour=0, minute=0, second=0)
r = db.record_items_col.find({"serial_id": 100})

print(r.count())
item = r[0]
return_str = f'[传送门{item["serial_id"]}]<a href={item["href"]}>{item["title"]}</a>'
print(return_str)
"""
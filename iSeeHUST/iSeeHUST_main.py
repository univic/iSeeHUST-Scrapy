
import os
import time
import json
import logging
import datetime
import hashlib
import flask
from flask import send_from_directory
from flask import Flask, request, make_response
import iSeeHUST.WeChatDispatch as WeChatDispatch
import iSeeHUST.DB
from conf.configs import CONFIGS


sLogger = logging.getLogger(__name__)

try:
    os.environ['TZ'] = 'Asia/Shanghai'  # 修改服务器时区为UTC+8
    time.tzset()
    sLogger.info('TZ SET')
except AttributeError as e:
    sLogger.info('TZ NOT SET')    # 该参数仅存在于Linux，在本地测试环境则忽视此项
    pass

app = Flask(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@app.route('/show_entries')
def show_entries():

    # 连接数据库
    db = iSeeHUST.DB.DBConn()

    # 设置查询时间限制
    query_date_limiter = datetime.datetime.now() - datetime.timedelta(CONFIGS['APP_CONFIGS']["DEFAULT_DATE_RANGE"])
    query_date_limiter.replace(hour=0, minute=0, second=0)

    # 查询数据，并按日期组成新的dict
    entries = db.record_items_col.find({"item_date": {"$gt": query_date_limiter}})
    page_items = {}
    for item in entries:
        date_str = datetime.datetime.strftime(item["item_date"], "%Y-%m-%d")
        if date_str in page_items:
            page_items[date_str].append(item)
        else:
            page_items[date_str] = [item]

    # 传入结果集，渲染页面
    return flask.render_template('show_entries.html', entries=page_items)


@app.route('/wechat', methods=['POST', 'GET'])
def wechat():
    # TODO 上线部署，验证后台配置
    if request.method == 'GET':  # GET方式为微信的连接测试请求
        token = CONFIGS["WECHAT_CONFIGS"]["Token"]  # 公众号后台设置的token
        data = request.args  # 获取数据的各项属性
        signature = data.get('signature', '')
        timestamp = data.get('timestamp', '')
        nonce = data.get('nonce', '')
        echostr = data.get('echostr', '')
        token_list = [token, timestamp, nonce]
        token_list.sort()
        s = token_list[0] + token_list[1] + token_list[2]
        hascode = hashlib.sha1(s.encode('utf-8')).hexdigest()
        if signature == hascode:
            return echostr
        else:
            return ""
    else:
        rec = request.stream.read()  # 利用requests模块读取消息数据
        dispatcher = WeChatDispatch.MsgDispatcher(rec)  # 调用消息分发
        data = dispatcher.dispatch()
        if data == '':
            return 'success'    # 如果返回值为空字符串，则以success字符串告知微信消息接收成功，不作其它动作
        else:
            response = make_response(data)  # 调用flask make_response函数返回消息
            response.content_type = 'application/xml'
            sLogger.info("RETURN MSG SENT")
            return response


def json_to_dict(json_path):
    with open(json_path, 'r') as f:
        result = json.load(f)
    return result


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1037, debug=True, threaded=True)

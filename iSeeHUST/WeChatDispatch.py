# /usr/bin/env python3
# -*- coding: utf-8 -*-
# Author : univic

import time
import xml.etree.ElementTree as et
import iSeeHUST.WeChatReply as WeChatReply
import logging


def get_logger():
    logger = logging.getLogger('iSeeHUST.WeChatDispatch')
    return logger


sLogger = get_logger()


class MsgParser(object):

    def __init__(self, data):
        self.data = data
        self.et = ''
        self.user = ''
        self.master = ''
        self.msgtype = ''
        self.msgid = ''
        self.content = ''
        self.recognition = ''
        self.format = ''
        self.picurl = ''
        self.mediaid = ''
        self.event = ''

    def msg_parse(self):
        # 使用xml模块提取消息包含的用户信息和时间戳
        self.et = et.fromstring(self.data)
        self.user = self.et.find('FromUserName').text
        self.master = self.et.find('ToUserName').text
        self.user = self.et.find('FromUserName').text

        # 判断消息类别，当前只支持文本消息
        self.msgtype = self.et.find('MsgType').text

        if self.et.find('Content') is not None:
            self.content = self.et.find('Content').text
        else:
            self.content = ''
        if self.et.find('MsgId') is not None:
            self.msgid = self.et.find('MsgId')
        else:
            self.msgid = ''
        if self.et.find('Recognition') is not None:
            self.recognition = self.et.find('Recognition')
        else:
            self.recognition = ''
        if self.et.find('Format') is not None:
            self.format = self.et.find('Format')
        else:
            self.format = ''
        if self.et.find('PicUrl') is not None:
            self.picurl = self.et.find('PicUrl')
        else:
            self.picurl = ''
        if self.et.find('MediaId') is not None:
            self.mediaid = self.et.find('MediaId')
        else:
            self.mediaid = ''
        if self.et.find('Event') is not None:
            self.event = self.et.find('Event')
        else:
            self.event = ''

        return self  # 解析形成消息对象并将其返回


class MsgDispatcher(object):
    """
    调度用户消息处理过程，调用解析模块对消息数据进行解析
    """

    def __init__(self, data):
        parser = MsgParser(data).msg_parse()
        self.msg = parser                   # 收到的消息解析为可直接操纵的消息对象
        self.handler = MsgHandler(self.msg)   # 为消息对象分配Handler
        self.result = ""

    def dispatch(self):
        self.result = ""
        if self.msg.msgtype == 'text':
            self.result = self.handler.text_handle()  # 为文本消息分配文本处理器
        return self.result


class MsgHandler(object):

    def __init__(self, msg):
        self.msg = msg
        self.time = int(time.time())   # 消息时间戳

    def text_handle(self, user='', master='', time='', content=''):
        template = """
       <xml>
             <ToUserName><![CDATA[{}]]></ToUserName>
             <FromUserName><![CDATA[{}]]></FromUserName>
             <CreateTime>{}</CreateTime>
             <MsgType><![CDATA[text]]></MsgType>
             <Content><![CDATA[{}]]></Content>
       </xml>        
        """

        msg_content = self.msg.content.strip()  # 去除前后空格
        reply_text = WeChatReply.TextReplyDispatch(msg_content)  # 实例化消息回复对象，传消息字符串值，决定回复内容
        response = reply_text.reply_dispatch()  # 获得返回的消息
        if response == "":
            sLogger.info(f"EMPTY RESULT RETURNED FOR {msg_content}")
        elif response is None:
            response = "Ooops, 后台暂时无法处理你的请求，你可以稍后再试"
            sLogger.warning(f"INCONSISTENT BETWEEN TX({msg_content}) AND RX({response})")
        else:
            sLogger.info(f"TX MSG FOR {msg_content} CONSTRUCTED")

        # 决定返回的内容
        if response == "":
            result = ""
        else:
            result = template.format(self.msg.user, self.msg.master, self.time, response)
        return result

    def news_handle(self):
        return 'news'

    def music_handle(self):
        return 'music'

    def voice_handle(self):
        return 'voice'

    def image_handle(self):
        return 'image'

    def video_handle(self):
        return 'video'

    def short_video_handle(self):
        return 'shortvideo'

    def location_handle(self):
        return 'location'

    def link_handle(self):
        return 'link'

    def event_handle(self):
        return 'event'

import scrapy
import re
import time
import datetime
import logging
from urllib.parse import urlparse
from urllib.parse import urlunparse
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst

from ..items import NewsitembotItem

logger = logging.getLogger(__name__)


class HUSTCMLoader(ItemLoader):
    href_out = TakeFirst()
    title_out = TakeFirst()
    item_date_out = TakeFirst()


class HustcmSpider(scrapy.Spider):

    name = "hustcm"

    def start_requests(self):
        urls = [
            'http://cm.hust.edu.cn/zz_xwzx/xydt.htm',
            'http://cm.hust.edu.cn/zz_xwzx/xstz.htm',
            'http://cm.hust.edu.cn/zz_xwzx/tzgg.htm',
            'http://cm.hust.edu.cn/zz_xwzx/yyld.htm',
            'http://cm.hust.edu.cn/ss/zxdt.htm',
            'http://cm.hust.edu.cn/ss/zsxx.htm',
            'http://cm.hust.edu.cn/ss/jxgl.htm',
            'http://cm.hust.edu.cn/ss/xwsq.htm',
            'http://cm.hust.edu.cn/MPAcc/xwdt/zxdt.htm',
            'http://cm.hust.edu.cn/zyfz/zpxx.htm',
            'http://cm.hust.edu.cn/zyfz/sxxx.htm',
            'http://cm.hust.edu.cn/zyfz/zyfz.htm',
        ]

        for url in urls[:]:
            time.sleep(1)
            yield scrapy.Request(url=url, callback=self.parse)


    # 解析函数，接收downloader的下载结果response并解析成item数据单元
    def parse(self, response):

        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        # 解析URL域名
        parsed_url = urlparse(response.request.url)
        domain = urlunparse([parsed_url.scheme, parsed_url.netloc, '', '', '', ''])

        # 查找全部类名为listmb的列表元素其下的列表元素
        nodes = response.xpath('//div[@class="listmb"]//li')
        logging.info(f">>>>>>>>{response.request.url} : {len(nodes)}")

        # 查找类名为listma的div标签，解析栏目名称
        section_name = response.xpath('//div[@class="listma"]/text()').extract()[0]

        # 遍历列表元素，提取标题、超链接、日期等，使用item_loader将其封装进数据单元
        for node in nodes:
            item_loader = HUSTCMLoader(item=NewsitembotItem(), selector=node)
            item_loader.add_xpath('title', 'a/@title')
            item_loader.add_value("tags", ["管理学院", section_name])

            # 将str类型日期转换为Datetime类型
            date_str = node.xpath('span/text()').extract()[0]
            date_str = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            item_loader.add_value('item_date', date_str)

            href = node.xpath('a/@href').extract()[0]
            # 调用url_convert函数将URL相对路径转换为绝对路径
            if domain not in href:
                href = self.url_convert(domain, href)

            item_loader.add_value('href', href)
            yield item_loader.load_item()

    # 正则匹配..开头的相对路径并使用域名替换
    @staticmethod
    def url_convert(domain, raw_url):
        p = re.compile(r'^(\.\./)*')
        rel_url = re.sub(p, '/', raw_url)
        converted_url = domain + rel_url
        return converted_url

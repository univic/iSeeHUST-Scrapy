# iSeeHUST-Scrapy

#### 项目介绍
iSeeHUST-Scrapy是一个基于Scrapy、Flask和MongoDB的爬虫项目，其主要用途是爬取关山口某高校的校园网站更新条目。
鉴于许多官方网站性质的站点都具备相似的内容结构，其也可用于爬取各类政府/机构网站。

此爬虫项目的主要目的是检测给定网站页面的更新，并且获取对应更新条目的标题和超链接。

#### 环境要求
本项目需配合MongoDB和Python3使用，建议的版本为：
>MongoDB > 3.2

>Python > 3.6

本项目推荐使用一个独立的python虚拟环境，可以在项目部署目录通过`python -m venv venv`命令创建

并通过如下命令激活虚拟环境

`. /your_project_path/venv/bin/activate`(Linux)

`your_project_path\venv\Scripts activate`(Windows)

#### 安装和部署

在项目根目录使用`pip install setup.py`命令安装相应的依赖包

在`WebMonPara.py`中配置与数据库连接相关的参数，例如：

在成功连接数据库后，项目将在第一次运行时创建所需的数据库和数据集

#### 新增一个爬虫

#### 查看爬取到的信息


##### 使用SNMP

##### 使用网页服务

项目基于Flask和Jinjia2提供有限的网页服务能力，如开启，则将利用Flask自带的Web服务响应Web请求。如有需要可自行搭建Web服务，Flask自带的Web服务不建议在生产环境下使用。

##### 使用微信公众平台


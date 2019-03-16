# iSeeHUST-Scrapy

#### 项目介绍
iSeeHUST-Scrapy是一个基于Scrapy、Flask和MongoDB的爬虫项目，其主要用途是爬取关山口某高校的校园网站更新条目。
鉴于许多官方网站性质的站点都具备相似的内容结构，其也可用于爬取各类政府/机构网站。

#### 环境要求
本项目需配合MongoDB和Python3使用，建议的版本为：
>MongoDB 3.2

>Python 3.6.8

本项目推荐使用一个独立的python虚拟环境，可以在项目部署目录通过`python -m venv venv`命令创建

并通过如下命令激活虚拟环境

`. /your_project_path/venv/bin/activate`(Linux)
`your_project_path\venv\Scripts activate`(Windows)

#### 安装和部署

在项目根目录使用`pip install setup.py`命令安装相应的依赖包

在`WebMonPara.py`中配置与数据库连接相关的参数，例如：

#### 新增一个爬虫
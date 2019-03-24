from setuptools import setup

setup(
    name='iSeeHUST-Scrapy',
    version='0.2',
    author='Wenfeng Zhong',
    author_email='xyzhgwf@outlook.com',
    packages=['iSeeHUST', 'NewsItemBot'],
    include_package_data=True,
    install_requires=[
        'flask',
        'scrapy',
        'pymongo',
        'bson',
        'Twisted'
    ],
)

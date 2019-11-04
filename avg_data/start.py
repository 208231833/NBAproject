#coding=utf-8
"""
调用这个方法生成球员的职业生涯的平均数据
"""
from scrapy.cmdline import execute
execute("scrapy crawl avg_get".split())

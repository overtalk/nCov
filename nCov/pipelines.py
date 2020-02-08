# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from .items import NCovOverall, NCovProvince, NCovArea
from .mongo.mongo import Config, MongoDB


class NCovOverallPipeline(object):
    conn = MongoDB(c=Config(db='ncov', host='127.0.0.1', port=27017))

    def process_item(self, item, spider):
        if isinstance(item, NCovOverall):
            self.conn.insert("overall", dict(item))
        return item


class NCovProvincePipeline(object):
    conn = MongoDB(c=Config(db='ncov', host='127.0.0.1', port=27017))

    def process_item(self, item, spider):
        if isinstance(item, NCovProvince):
            self.conn.insert("province", dict(item))
        return item


class NCovAreaPipeline(object):
    conn = MongoDB(c=Config(db='ncov', host='127.0.0.1', port=27017))

    def process_item(self, item, spider):
        if isinstance(item, NCovArea):
            self.conn.insert("area", dict(item))
        return item

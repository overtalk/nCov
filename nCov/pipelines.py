# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from .items import NCovOverall


class NcovPipeline(object):
    def process_item(self, item, spider):
        return item


class NCovOverallPipeline(object):
    host = ''
    port = ''
    db = ''
    conn = pymongo.MongoReplicaSetClient

    def __init__(self, db='ncov', host='127.0.0.1', port=27017):
        self.db = db
        self.port = port
        self.host = host
        self.conn = pymongo.MongoClient(host=self.host, port=self.port)[self.db]

    def process_item(self, item, spider):
        if isinstance(item, NCovOverall):
            self.conn["overall"].insert(dict(item))
        return item

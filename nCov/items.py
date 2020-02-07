# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class NCovOverall(Item):
    confirmedCount = Field()
    suspectedCount = Field()
    curedCount = Field()
    deadCount = Field()
    seriousCount = Field()
    suspectedIncr = Field()
    confirmedIncr = Field()
    curedIncr = Field()
    deadIncr = Field()
    seriousIncr = Field()
    pass


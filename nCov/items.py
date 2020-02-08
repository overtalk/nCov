# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
from scrapy import Item, Field


class NCovOverall(Item):
    crawlTS = Field()
    crawlDate = Field()
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


class NCovProvince(Item):
    crawlTS = Field()
    crawlDate = Field()
    locationId = Field()
    countryType = Field()
    country = Field()
    provinceId = Field()
    provinceName = Field()
    confirmedCount = Field()
    suspectedCount = Field()
    curedCount = Field()
    deadCount = Field()
    pass


class NCovArea(Item):
    crawlTS = Field()
    crawlDate = Field()
    locationId = Field()
    provinceName = Field()
    cityName = Field()
    confirmedCount = Field()
    suspectedCount = Field()
    curedCount = Field()
    deadCount = Field()
    pass


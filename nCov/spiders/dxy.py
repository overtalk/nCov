# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from bs4 import BeautifulSoup
import re
import json
from ..items import NCovOverall, NCovProvince, NCovArea
import datetime

country_type = {
    1: '中国'
}

class DxySpider(Spider):
    name = 'dxy'
    start_urls = ['https://3g.dxy.cn/newh5/view/pneumonia']
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 '
                      'Safari/537.36'
    }

    def __init__(self):
        self.crawl_timestamp = int()
        self.crawl_date = ""

    def start_requests(self):
        self.crawl_timestamp = int(datetime.datetime.timestamp(datetime.datetime.now()) * 1000)
        self.crawl_date = datetime.date.today().strftime("%Y-%m-%d")
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse, headers=self.header)

    def parse(self, response):
        data = response.body
        soup = BeautifulSoup(data, "html5lib")
        overall_information = re.search(r'\{("id".*?)\]\}',
                                        str(soup.find('script', attrs={'id': 'getStatisticsService'})))
        province_information = re.search(r'\[(.*?)\]',
                                         str(soup.find('script', attrs={'id': 'getListByCountryTypeService1'})))
        area_information = re.search(r'\[(.*)\]', str(soup.find('script', attrs={'id': 'getAreaStat'})))
        abroad_information = re.search(r'\[(.*)\]',
                                       str(soup.find('script', attrs={'id': 'getListByCountryTypeService2'})))
        news = re.search(r'\[(.*?)\]', str(soup.find('script', attrs={'id': 'getTimelineService'})))
        yield self.overall_parser(overall_information=overall_information)
        for item in self.province_parser(province_information=province_information):
            yield item
        for item in self.area_parser(area_information=area_information):
            yield item
        self.abroad_parser(abroad_information=abroad_information)
        # self.news_parser(news=news)
        return

    def overall_parser(self, overall_information):
        overall_information = json.loads(overall_information.group(0))
        item = NCovOverall()
        item["crawlTS"] = self.crawl_timestamp
        item["crawlDate"] = self.crawl_date
        # count
        item["confirmedCount"] = overall_information["confirmedCount"]
        item["suspectedCount"] = overall_information["suspectedCount"]
        item["curedCount"] = overall_information["curedCount"]
        item["deadCount"] = overall_information["deadCount"]
        item["seriousCount"] = overall_information["seriousCount"]
        # increase
        item["confirmedIncr"] = overall_information["confirmedIncr"]
        item["suspectedIncr"] = overall_information["suspectedIncr"]
        item["curedIncr"] = overall_information["curedIncr"]
        item["deadIncr"] = overall_information["deadIncr"]
        item["seriousIncr"] = overall_information["seriousIncr"]
        return item

    def province_parser(self, province_information):
        items = []
        provinces = json.loads(province_information.group(0))
        for province in provinces:
            item = NCovProvince()
            item["crawlTS"] = self.crawl_timestamp
            item["crawlDate"] = self.crawl_date
            item["locationId"] = province["locationId"]
            item["countryType"] = province["countryType"]
            item["country"] = country_type.get(province['countryType'])
            item["provinceId"] = province["provinceId"]
            item["provinceName"] = province["provinceName"]
            item["confirmedCount"] = province["confirmedCount"]
            item["confirmedCount"] = province["confirmedCount"]
            item["suspectedCount"] = province["suspectedCount"]
            item["curedCount"] = province["curedCount"]
            item["deadCount"] = province["deadCount"]
            items.append(item)
        return items

    def area_parser(self, area_information):
        items = []
        area_information = json.loads(area_information.group(0))
        for area in area_information:
            for city_info in area['cities']:
                item = NCovArea()
                item["provinceName"] = area["provinceName"]
                item["crawlTS"] = self.crawl_timestamp
                item["crawlDate"] = self.crawl_date
                item["cityName"] = city_info["cityName"]
                item["locationId"] = city_info["locationId"]
                item["confirmedCount"] = city_info["confirmedCount"]
                item["suspectedCount"] = city_info["suspectedCount"]
                item["curedCount"] = city_info["curedCount"]
                item["deadCount"] = city_info["deadCount"]
                items.append(item)
        return items

    def abroad_parser(self, abroad_information):
        cccc = 0
        countries = json.loads(abroad_information.group(0))
        for country in countries:
            country.pop('id')
            country.pop('tags')
            country.pop('countryType')
            country.pop('provinceId')
            country['country'] = country.get('provinceName')
            country['provinceShortName'] = country.get('provinceName')
            country.pop('cityName')
            country.pop('sort')
            country['comment'] = country['comment'].replace(' ', '')
            country['updateTime'] = self.crawl_timestamp
            if cccc == 0:
                cccc = cccc + 1
                print("country = ", country)

    def news_parser(self, news):
        news = json.loads(news.group(0))
        for _news in news:
            _news.pop('pubDateStr')
            _news['crawlTime'] = self.crawl_timestamp
            print("news = ", news)

    def rumor_parser(self, rumors):
        for rumor in rumors:
            rumor.pop('score')
            rumor['body'] = rumor['body'].replace(' ', '')
            rumor['crawlTime'] = self.crawl_timestamp
            print("rumor = ", rumor)

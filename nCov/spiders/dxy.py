# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from bs4 import BeautifulSoup
import re
import json
from ..items import NCovOverall

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

    def start_requests(self):
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
        item = self.overall_parser(overall_information=overall_information)
        yield item
        # self.province_parser(province_information=province_information)
        # self.area_parser(area_information=area_information)
        # self.abroad_parser(abroad_information=abroad_information)
        # self.news_parser(news=news)
        return


    def overall_parser(self, overall_information):
        overall_information = json.loads(overall_information.group(0))
        overall_information.pop('id')
        overall_information.pop('createTime')
        overall_information.pop('modifyTime')
        overall_information.pop('imgUrl')
        overall_information.pop('deleted')
        overall_information['countRemark'] = overall_information['countRemark'].replace(' 疑似', '，疑似').replace(' 治愈',
                                                                                                              '，治愈').replace(
            ' 死亡', '，死亡').replace(' ', '')
        item = NCovOverall()
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
        print(item)
        return item



    def province_parser(self, province_information):
        provinces = json.loads(province_information.group(0))
        for province in provinces:
            province.pop('id')
            province.pop('tags')
            province.pop('sort')
            province['comment'] = province['comment'].replace(' ', '')
            province['crawlTime'] = self.crawl_timestamp
            province['country'] = country_type.get(province['countryType'])
            print("province = ", province)

    def area_parser(self, area_information):
        area_information = json.loads(area_information.group(0))
        for area in area_information:
            area['comment'] = area['comment'].replace(' ', '')
            area['country'] = '中国'
            area['updateTime'] = self.crawl_timestamp
            print("area = ", area)

    def abroad_parser(self, abroad_information):
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

from base64 import encode
from email import header
from ntpath import join
from wsgiref.headers import Headers

from bs4 import BeautifulSoup
from NewsSpiders.items import NewsItem
import utils
import scrapy
import requests
import re



def get_joiner_and_place(text):
    sentences = utils.get_sentences(texts=text)
    # words, nerss = fool.analysis(sentences)
    joiners = list()
    places = list()
    # for ners in nerss:
    #     for ner in ners:
    #         if ner[2] in ["person","org"]:
    #             joiners.append({"type":ner[2],"content":ner[3]})
    #         elif ner[2]  in ["location"]:
    #             places.append(ner[3])
    return joiners,places

class CctvSpider(scrapy.Spider):
    name = 'cctv'
    allowed_domains = ['cctv.com']
    start_urls = ['https://military.cctv.com/data/index.json']
    def start_requests(self):
        headers = utils.headers
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse,headers=headers)

    def parse(self, response):
        news_list = response.json()['rollData']
        items = []
        for news in news_list:
            item = NewsItem()
            item['title'] = news['title']
            item['url'] = news['url']
            item['content'] = news['description']
            item['time'] = news['dateTime'][0:10]
            item['joiner'],item['place'] = get_joiner_and_place(news['url'])
            items.append(item)
        return items

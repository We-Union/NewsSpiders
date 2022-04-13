from email import header
from wsgiref.headers import Headers
from NewsSpiders.items import NewsItem
import utils
import scrapy


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
            print(news)
            item = NewsItem()
            item['title'] = news['title']
            item['url'] = news['url']
            item['content'] = news['description']
            item['time'] = news['dateTime'][0:10]
            item['joiner'] = list()
            item['place'] = list()
            items.append(item)
        return items

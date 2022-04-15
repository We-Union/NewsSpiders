from ntpath import join
from numpy import place
import scrapy
import utils
from NewsSpiders.items import NewsItem
from bs4 import BeautifulSoup
import re
import requests




def get_main_text(soup):
    text = ""
    soup = soup.find("div",class_ = "mw-parser-output")
    for p in soup.find_all("p"):
        text += p.get_text()
    return text


class WikipediaSpider(scrapy.Spider):
    name = 'wikipedia'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['http://en.wikipedia.org/wiki']
    def start_requests(self):
        event_lables = utils.read_events()
        headers = utils.headers
        i = 0
        for event_lable in event_lables:
            yield scrapy.Request(url=self.start_urls[0]+"/"+event_lable, callback=self.parse,headers=headers)
            # if i > 10:
            #     return
            # i += 1

    def parse(self, response):
        item = NewsItem()
        soup = BeautifulSoup(response.text)
        item['title'] = soup.head.title.get_text()[0:-12]
        item['url'] = response.url
        item['content'] = get_main_text(soup)

        contents = soup.find("div",class_ = "mw-parser-output")
        contents = contents.find_all("p")
        for i in range(len(contents)):
            if len(contents[i].get_text()) > 5:
                 item['desc'] = contents[i].get_text().replace("\n","")
                 break    

        item['infobox'] = str(soup.find("table",class_ = re.compile("infobox")))
        return item

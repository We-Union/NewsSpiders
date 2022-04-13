import scrapy
import utils
from NewsSpiders.items import NewsItem
from bs4 import BeautifulSoup
import re

class WikipediaSpider(scrapy.Spider):
    name = 'wikipedia'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['http://en.wikipedia.org/wiki']
    def start_requests(self):
        event_lables = utils.read_events()
        print(len(event_lables))
        headers = utils.headers
        i = 0
        for event_lable in event_lables:
            print("-----------------------",event_lable)
            yield scrapy.Request(url=self.start_urls[0]+"/"+event_lable, callback=self.parse,headers=headers)
            # if i > 20:
            #     return
            i += 1

    def parse(self, response):
        item = NewsItem()
        soup = BeautifulSoup(response.text)
        item['title'] = soup.head.title.get_text()[0:-12]
        item['url'] = response.url
        contents = soup.find("div",class_ = "mw-parser-output")
        contents = contents.find_all("p")
        for i in range(len(contents)):
            if contents[i].get_text() != "\n":
                 item['content'] = contents[i].get_text().replace("\n","")
                 break       
        # print(content.get_text())

        infobox = soup.find("table",class_ = re.compile("infobox"))
        if infobox is not None:
            trs = infobox.find_all("tr")
            item['time'] = ""
            item['place'] = ""
            for tr in trs:
                ths = tr.find_all("th")
                tds = tr.find_all("td")
                if len(ths) == 1 and len(tds)==1:
                    th = ths[0].get_text()
                    td = tds[0].get_text()
                    if th.find("Date") != -1:
                        item['time'] = td

                    if th.find("Location") != -1:
                        item['place'] = td.split(",")



        item['joiner'] = list()
        return item

from ntpath import join
from numpy import place
import scrapy
import utils
from NewsSpiders.items import NewsItem
from bs4 import BeautifulSoup
import re
import stanza
import requests

nlp = stanza.Pipeline(lang='en', processors='tokenize,ner',use_gpu=True)

def get_sentences(url = None,texts = None):
    if url is not None:
        response = requests.get(url,headers=utils.headers)
        if response.status_code != 200:
            return None,None
        html = response.text
        print(html)
        soup = BeautifulSoup(html)
        texts = soup.get_text()
    sentences = re.split("\.|\?|!|;|:", texts)
    results = list()
    for sentence in sentences:
        if len(sentence) > 1:
            results.append(sentence)
    return results

def get_joiner_from_sentence(sent):
    sentences = get_sentences(texts=sent)
    text_to_type = dict()
    text_cnt = dict()
   
    for sentence in sentences:
        doc = nlp(sentence)
        for ent in doc.ents:
            if ent.type in ['PERSON','NORP','FACILITY','ORGANIZATION','GPE']:
                if ent.text in text_to_type:
                    text_cnt[ent.text] += 1
                else:
                    text_to_type[ent.text] = ent.type
                    text_cnt[ent.text] = 1
                
    text_cnt = sorted(text_cnt.items(), key = lambda kv:(kv[1], kv[0]),reverse=True)     
    i = 0
    joiners = list()
    for text_tuble in text_cnt:
        # text_tule : [("hzl",1)]
        text = text_tuble[0]
        joiners.append({"type":text_to_type[text],"content":text})
        i += 1
        if i > 10:
            break
        
    return joiners



def get_time_place(sent):
    sentences = get_sentences(texts=sent)
    times = list()
    places = list()
   
    for sentence in sentences:
        doc = nlp(sentence)
        for ent in doc.ents:
            if ent.type in ['FACILITY','GPE','LOCATION']:
                places.append(ent.text)
            if ent.type in ['DATE','TIME']:
                times.append(ent.text)

    return times,places

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
            print("-----------------------",event_lable)
            yield scrapy.Request(url=self.start_urls[0]+"/"+event_lable, callback=self.parse,headers=headers)
            if i > 10:
                return
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
        

        item['time'] = []
        item['place'] = []
        infobox = soup.find("table",class_ = re.compile("infobox"))
        if infobox is not None:
            trs = infobox.find_all("tr")
            for tr in trs:
                ths = tr.find_all("th")
                tds = tr.find_all("td")
                if len(ths) == 1 and len(tds)==1:
                    th = ths[0].get_text()
                    td = tds[0].get_text()
                    if th.find("Date") != -1:
                        item['time'] = [td]
                    if th.find("Location") != -1:
                        item['place'] = td.split(",")
            # print(infobox.get_text())
            if len(item['time']) == 0  or  len(item['place']) == 0:

                time,place = get_time_place(infobox.get_text())
                
                if len(item['time']) == 0:
                    item['time'] = time
                if len(item['place']) == 0:
                    item['place'] = place


        joiner = get_joiner_from_sentence(get_main_text(soup))
        item["joiner"] = joiner


       
        
        return item

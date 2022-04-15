import re
from bs4 import BeautifulSoup
import stanza
import requests
import json
from tqdm import tqdm

MAX_JOINER = 10

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

def get_sentences(url = None,texts = None):
    if url is not None:
        response = requests.get(url,headers=utils.headers)
        if response.status_code != 200:
            return None,None
        html = response.text
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
        if i >= MAX_JOINER:
            break
        
    return joiners


def process_one(data):
    item = dict()
    item['title'] = data['title']
    item['url'] = data['url']
    item['desc'] = data['desc']
    item['time'] = list()
    item['place'] = list()
    item['joiner'] = list()

    infobox = BeautifulSoup(data['infobox'])
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


        if len(item['time']) == 0  or  len(item['place']) == 0:

            time,place = get_time_place(infobox.get_text())
            
            if len(item['time']) == 0:
                item['time'] = time
            if len(item['place']) == 0:
                item['place'] = place


    item["joiner"] = get_joiner_from_sentence(data["content"])
    return item


def read_wikipedia_data():
    with open("wikipedia.json",'r',encoding="utf-8") as f:
        load_dict = json.load(f)
        return load_dict

def main():

    datas = read_wikipedia_data()
    print("total:",len(datas))
   
    with open("results.json",'a',encoding="utf-8") as f:
        for i in tqdm(range(len(datas))):
            result = process_one(datas[i])
            f.write(json.dumps(result)+"\n")
            f.flush()

if __name__ == "__main__":
    nlp = stanza.Pipeline(lang='en', processors='tokenize,ner',use_gpu=True)
    main()
headers={
'accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'zh-CN,zh;q=0.9',
'sec-fetch-mode': 'cors',
"sec-fetch-site": 'same-origin',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
'x-requested-with': 'XMLHttpRequest'
}
import requests
import re
from bs4 import BeautifulSoup

def read_events():
    event_labels = []
    with open('events.txt', 'r',encoding="utf-8") as f:
        for line in f:
            event_labels.append(line.strip())
    return event_labels


def get_sentences(url = None,texts = None):
    if url is not None:
        response = requests.get(url,headers=headers)
        if response.status_code != 200:
            return None,None
        html = response.text
        print(html)
        soup = BeautifulSoup(html)
        texts = soup.get_text()
    sentences = re.split("。|\.|，|\?|？|!|！|；|;|:|：|—|-", texts)
    results = list()
    for sentence in sentences:
        if len(sentence) > 1:
            results.append(sentence)
    return results
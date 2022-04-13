headers={
'accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'zh-CN,zh;q=0.9',
'sec-fetch-mode': 'cors',
"sec-fetch-site": 'same-origin',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
'x-requested-with': 'XMLHttpRequest'
}


def read_events():
    event_labels = []
    with open('events.txt', 'r',encoding="utf-8") as f:
        for line in f:
            event_labels.append(line.strip())
    return event_labels
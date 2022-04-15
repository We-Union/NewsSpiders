# 事件知识谱图爬虫

## 如何使用

1. 克隆本项目到本地
2. 运行`pip install -r requirements.txt`安装依赖
3. 打开一个python终端，运行如下代码下载数据：

```python
import stanza
stanza.download('en') # download English model
```


4. 在项目根目录输入`scrapy crawl wikipedia -o wikipedia.json  -s LOG_FILE=all.log`命令即可运行爬虫。
5. 运行`progress.py`可以对爬取的数据进行处理。处理的结果输出在results.json中。为了方便从中途中断，再次运行的时候可以利用之前爬取的数据，运行的时候会采用追加的方式写入文件，每条结果会输出一行："{...}"（不包括引号）。




## 使用的主要第三方库

+ scrapy : 负责爬取网页
+ stanza : 负责抽取参与者


## 爬虫列表

### 1. wikipedia

可以从events.txt获取维基百科对应的英文事件名称，让后使用scrapy访问网页，抽取事件的时间、内容、名称、URL、地点等信息。

#### 事件抽取方式：


|字段|抽取方式|
| -- | -- |
|tile|直接读取维基百科标题|
|desc|读取维基百科第一段|
|date|读取维基百科右侧列表的日期|
|location|读取维基百科右侧表格的location|
|joiner|识别出维基百科全文里面的所有实体，取出现次数最多的前20个|

### 2. cctv






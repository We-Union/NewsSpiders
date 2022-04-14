# 事件知识谱图爬虫

## 如何使用

1. 克隆本项目到本地
2. 运行`pip install -r requirements.txt`安装依赖
3. 打开一个python终端，运行如下代码下载数据：

```python
import stanza
stanza.download('en') # download English model
```


4. 在项目根目录输入`scrapy crawl wikipedia -o wikipedia.json`命令即可运行。


## 爬虫名称对照表

|爬虫名|英文名称|
| -- | -- |
|维基百科|wikipedia|

可以从events.txt获取事件名称，抽取事件的时间、内容、名称、URL、地点等信息。


## 使用的主要第三方库

+ scrapy : 负责爬取网页
+ stanza : 负责抽取参与者

## 事件抽取方式如下：

### title

直接读取维基百科标题

### desc

读取维基百科第一段

### date

读取维基百科右侧列表的日期

### location

读取维基百科右侧表格的location

### joiner

识别出维基百科全文里面的所有实体，取出现次数最多的前20个




import scrapy
from bs4 import BeautifulSoup
from day028.items import Day028Item

class PttarticleSpider(scrapy.Spider):
    name = 'pttarticle'
    def __init__(self ,start_urls , filename=None):
        self.cookies = {'over18':'1'}
        self.start_urls =start_urls
        self.filename = filename
        super().__init__()

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url,callback=self.parse,cookies=self.cookies)
            
    def parse(self, response):
        if response.status != 200:
            print('Error,we can\'t open this url')
            print('{}'.format(response.url))
            return
        
        soup = BeautifulSoup(response.text)
        
        main_content = soup.find('div',id="main-content")
        
        #截取作者、看板、標題和時間
        author = main_content.find_all(class_="article-meta-value")[0].text
        tag = main_content.find_all(class_="article-meta-value")[1].text
        title = main_content.find_all(class_="article-meta-value")[2].text
        datetime = main_content.find_all(class_="article-meta-value")[3].text
        
        #利用extract()做刪除
        #因為內文不在tag中可截取，所以把不需要的都用extract()做除去動作
        meta = main_content.find_all('div',class_='article-metaline')
        for m in meta:
            m.extract()
        right_meta = main_content.find_all('div',class_='article-metaline-right')
        for m in right_meta:
            m.extract()
        push = main_content.find_all('div',class_='push')
        for m in push:
            m.extract()

        #整理文章資訊
        data = Day028Item()
        data['url'] = response.url
        data['author'] = author
        data['title'] = title
        data['tag'] = tag
        data['date'] = datetime
        data['content'] = main_content.text
        yield data
        
        
        


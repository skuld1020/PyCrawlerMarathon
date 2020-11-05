import scrapy
from bs4 import BeautifulSoup
from day029.items import Day029Item



class PttarticleSpider(scrapy.Spider):
    name = 'PttArticle'
    allowed_domains = ['www.ptt.cc']
    start_urls = ['https://www.ptt.cc/bbs/Gossiping/index.html',
                  'https://www.ptt.cc/bbs/movie/index.html']
    cookies = {'over18':'1'}
    
        
    def start_requests(self):
        yield scrapy.Request(url =self.start_urls, callback = self.parse, cookies = self.cookies)
        
    
    def parse(self, response):
        # 取得列表中的清單主體
        soup = BeautifulSoup(response.text)
        main_list = soup.find('div', class_='bbs-screen')

        # 依序檢查文章列表中的 tag, 遇到分隔線就結束，忽略這之後的文章
        for div in main_list.findChildren('div', recursive=False):
            class_name = div.attrs['class']

            # 遇到分隔線要處理的情況
            if class_name and 'r-list-sep' in class_name:
                self.log('Reach the last article')
                break

            # 遇到目標文章
            if class_name and 'r-ent' in class_name:
                div_title = div.find('div', class_='title')
                a_title = div_title.find('a', href=True)
                # 如果文章已經被刪除則跳過
                if not a_title or not a_title.has_attr('href'):
                    continue
                article_URL = urljoin(self.host, a_title['href'])
                article_title = a_title.text
                self.log('Parse article {}'.format(article_title))
                yield scrapy.Request(url=article_URL,
                                     callback=self.article_parse,
                                     cookies=self.cookies)
        
        
    def article_parse(self,response):
        if response.status != 200:
            print('Error,we can\'t open this url')
            print('{}'.format(response.url))
            return
        
        
        #整理文章資訊
        item = Day029Item()
        item['tag'] = response.xpath('//div[@id="main-container"]//div[2]/span[@class="article-meta-value"]/text()').get()
        item['title'] = response.xpath('//div[@id="main-container"]//div[3]/span[@class="article-meta-value"]/text()').get()
        item['datetime'] = response.xpath('//div[@id="main-container"]//div[4]/span[@class="article-meta-value"]/text()').get()
        item['content'] = response.xpath('//div[@id="main-content"]/text()').get()
        item['url'] = response.url
        item['author'] = response.xpath('//div[@id="main-container"]//div[1]/span[@class="article-meta-value"]/text()').get()
       
                      
        yield item
        


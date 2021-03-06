import scrapy
from d025work.items import D025WorkItem



class EttodaySpider(scrapy.Spider):
    name = 'ettoday'
    allowed_domains = ['www.ettoday.net']
    start_urls = ['https://www.ettoday.net/news/20201004/1824032.htm',
                  'https://www.ettoday.net/news/20201104/1846312.htm']

    def parse(self, response):
        if response.status !=200:
            print('Error!')
            print('{}'.format(response.url))
            return
        
        item = D025WorkItem()
        item['title'] = response.xpath('//title/text()').get()
        item['content'] = response.xpath('//article//div[@class="story"]/p/text()').getall()
        yield item
        
        

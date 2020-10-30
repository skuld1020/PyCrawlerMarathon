import scrapy


class EttodaySpider(scrapy.Spider):
    name = 'ettoday'
    allowed_domains = ['www.ettoday.net']
    start_urls = ['https://www.ettoday.net/news/20201004/1824032.htm']

    def parse(self, response):
        if response.status !=200:
            print('Error!')
            print('{}'.format(response.url))
            return
        
        title = response.xpath('//title/text()').get()
        content = response.xpath('//article//div[@class="story"]/p/text()').getall()
        print(title)
        print(content)
        
        

import scrapy
import requests
import schedule 
import time 
from scrapy import cmdline 

class MashreghSpider(scrapy.Spider):
    name = "tasnim"
    allowed_domains = ["www.tasnimnews.com"]
    start_urls = ["https://www.tasnimnews.com/fa/service/1392/%D8%AD%D9%88%D8%A7%D8%AF%D8%AB"]

    def parse(self, response):
        news_list = response.css('article.list-item')
        
        for news in news_list:
            title = news.css('h2.title::text').get()
            link = news.css('a::attr(href)').get()
            # yield { 'title' : title, 'link' : link }
            yield response.follow(link, callback=self.parse_fetched_link)

    def parse_fetched_link(self, response):
        text_list = response.selector.xpath('/html/body/div/main/div/section[1]/div/section[1]/article/div[3]/p//text()').getall()
        title = response.css('h1.title::text').get()
        img = response.css('img.img-responsive::attr(src)').get()

    
        result = 'STARTP' + text_list[2].replace('،','',1) + "\n\n"
        for i in range(3, len(text_list) - 1) :
            result += 'STARTP' + text_list[i].replace('،','',1) + "\n\n"

        yield {'title' : title, 
               'text': result, 
               'image':img,
               'url':response.request.url,
               }
               
        


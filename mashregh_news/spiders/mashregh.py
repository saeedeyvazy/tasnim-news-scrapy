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
        text_list = response.css('div.story p::text')
        title = response.css('h1.title::text').get()
        img = response.css('img.img-responsive::attr(src)').get()

        # result = '<strong>&#x1F53A;</strong>' + '،'.join(text_list[1].get().split('،')[1:]) + "\n\n"    
        result = 'STARTP' + '،'.join(text_list[1].get().split('،')[1:]) + "\n\n"
        for i in range(2, len(text_list) - 1) :
            # result += '<strong>&#x1F53A;</strong>' + text_list[i].get() + "\n\n"
            result += 'STARTP' + text_list[i].get() + "\n\n"

        yield {'title' : title, 
               'text': result, 
               'image':img,
               'url':response.request.url,
               }
               
        


import psycopg2
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from datetime import datetime
import logging

class MashreghNewsPipeline:
    def process_item(self, item, spider):
        return item


class SavingToPostgresPipeline(object):
    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.connection = psycopg2.connect(database="saeed",
                        host="172.17.0.2",
                        user="saeed",
                        password="saeed",
                        port="5432")
        self.connection.autocommit=True
        self.cursor = self.connection.cursor()

    def process_item(self, item, spider):
        try:
            self.cursor.execute('''INSERT INTO NEWS(URL,TITLE, TEXT, IMG,NEWS_DATE ) VALUES (%s,%s,%s,%s,%s)''',
                                (item['url'],item['title'],item['text'], item['image'],datetime.now()))
            return item
        except BaseException as e:
            logging.error('Error In SavingToPostgresPipeline: %s', e)
            self.connection.commit        

class DuplicateNewsPipeline:
    
    def __init__(self):
        self.seen_url = set()

    def process_item(self,item,spider):
        adapter = ItemAdapter(item)
        if adapter['title'] in self.seen_url:
            raise DropItem(f"Duplicate Item Found: {item!r}")   
        else:
            self.seen_url.add(adapter['title'])
            return item

# class SendNewsToEittaChannel:
#     EITAA_CHANNEL = "https://eitaayar.ir/api/bot214251:acaf875c-c4ec-45a6-8086-b1bbca85cb44/sendFile"
#     def __init__(self):
#         pass    

#     def process_item(self, item, spider):

#         params = {
#             'caption' : '<strong>&#x1F4E2;</strong>' + item['title'] + '\n\n' 
#             +item['text'],
#             'date':0,
#             'chat_id':'news_ruz',
#             'pin':'off',
#             'parse_mode':'html',
#             'file':item['image']
#         }
#         try:    
#             response = requests.post(url=self.EITAA_CHANNEL, params=params)
#             resp = response.json()
#             if resp['ok']:
#                 return item
#         except Exception as e:
#             logging.error('Failed to Send News To Eitta Channel: %s', e)
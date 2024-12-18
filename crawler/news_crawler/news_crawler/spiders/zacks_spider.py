import json
import scrapy
from datetime import datetime
from scrapy import Request
from collections.abc import Iterable
from parsel import Selector
from news_crawler.news_crawler.user_agents import get_random_user_agent

class ZacksSpider(scrapy.Spider):
    name = 'zacks'
    
    def __init__(self, latest_published_at: datetime, max_page: int = 125):
        self.latest_published_at = latest_published_at
        self.max_page = max_page
    
    def start_requests(self) -> Iterable[Request]:
        yield scrapy.Request(
            url = 'https://www.zacks.com/blog/archive.php?page=1&type=json&g=69', 
            headers = get_random_user_agent(),
            meta = {"page" : 1}
        )
            
    def parse(self, response):
        stop_crawl_flag = False
        
        response_json = json.loads(response.body)
        selector = Selector(text = response_json['response'])
        
        articles = selector.xpath("//div[@class='listitem']")
        for article in articles:
            article_date_str = article.xpath(".//time/text()").get().replace("Published on ", "").strip()
            article_date = datetime.strptime(article_date_str, "%B %d,%Y")
            
            if self.latest_published_at and self.latest_published_at > article_date:
                stop_crawl_flag = True
                
            article_link = article.xpath(".//h1[@class='truncated_text_single']/div/a/@href").get()
            yield response.follow(
                url = 'https://www.zacks.com' + article_link, 
                headers = get_random_user_agent(), 
                meta={'dont_redirect': True}, 
                callback = self.parse_article, 
                errback = self.handle_redirect
            )
        
        current_page = response.meta["page"]
        if not stop_crawl_flag and current_page < self.max_page:
            next_page = current_page + 1
            yield scrapy.Request(
                url = f"https://www.zacks.com/blog/archive.php?page={next_page}&type=json&g=69",
                headers = get_random_user_agent(),
                callback = self.parse,
                meta = {"page" : next_page}
            )
            
    def parse_article(self, response):
        article_dict = {}
        
        article_dict['country'] = 'USA'
        article_dict['title'] = response.xpath("//section[@id='commentary_article']/article/h1/text()").get()
        
        img_src = response.xpath("//div[@class='main_body']/section[@id='commentary_article']/div[@class='article_banner']/img/@ll_src").get()
        article_dict['image_link'] = img_src if img_src is not None else ''
        
        article_dict['source'] = 'Zack\'s'
        
        texts = response.xpath("//div[@id='comtext']//text()[not(ancestor::a)]").getall()[2:]
        content = ''.join([text.strip() for text in texts])
        content = content.replace(' Quick Quote-', '')
        article_dict['content'] = content
        
        date_string = response.xpath("//header[@class='ticker-and-social-ribbon']/aside/p[@class='byline']/span/time/text()").get()
        article_dict['published_at'] = self.convert_datetime(date_string)
        article_dict['link'] = response.url
        
        yield article_dict
        
    def handle_redirect(self, redirect):
        if redirect.value.response.status == 302:
            self.logger.info(f"Retrying URL: {redirect.request.url} due to 302 status code")
            yield scrapy.Request(
                url = redirect.request.url, 
                headers = get_random_user_agent(),
                callback = self.parse_article, 
                meta = {'dont_redirect' : True}
            )
    
    def convert_datetime(self, datetime_str) -> str:
        datetime_object = datetime.strptime(datetime_str, "%B %d, %Y")
        return datetime_object.strftime("%Y-%m-%d %H:%M:%S")
        

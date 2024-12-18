import scrapy
from scrapy import Request
from collections.abc import Iterable
from datetime import datetime
from news_crawler.news_crawler.user_agents import get_random_user_agent

class BusinessInsiderSpider(scrapy.Spider):
    name = 'businessinsider'
    
    def __init__(self, latest_published_at: datetime, max_page: int = 200) -> None:
        self.latest_published_at = latest_published_at
        self.max_page = max_page
    
    def start_requests(self) -> Iterable[Request]:
        yield scrapy.Request(
            url = "https://markets.businessinsider.com/news?p=1",
            headers = get_random_user_agent(),
            meta = {"page" : 1}
        )        

    def parse(self, response):
        stop_crawl_flag = False
        articles = response.xpath("//div[@class='latest-news__story']")
        for article in articles:
            article_date_str = article.xpath(".//time[@class='latest-news__date']/@datetime").get()
            article_date = datetime.strptime(article_date_str, "%m/%d/%Y %I:%M:%S %p")
            
            if self.latest_published_at and self.latest_published_at > article_date:
                stop_crawl_flag = True
            
            source = article.css('span.latest-news__source::text').get()
            if source == 'Business Insider':
                link = article.css('a.latest-news__link').attrib['href']
                yield response.follow(
                    url = link,
                    headers = get_random_user_agent(),
                    callback = self.parse_article
                )
                
        current_page = response.meta["page"]
        if not stop_crawl_flag and current_page < self.max_page:
            next_page = current_page + 1
            yield scrapy.Request(
                url = f"https://markets.businessinsider.com/news?p={next_page}",
                headers = get_random_user_agent(),
                callback = self.parse,
                meta = {"page" : next_page}
            )
    
    def parse_article(self, response):
        article_dict = {}

        article_dict['country'] = 'USA'
        article_dict['title'] = response.css('h1.post-headline::text').get()
        article_dict['image_link'] = response.css('figure.figure.image-figure-image div > img').attrib['src']
        article_dict['source'] = 'Business Insider'    
        
        content_str = response.xpath("normalize-space(//div[@class='content-lock-content'])").get()
        article_dict['content'] = content_str.replace('Advertisement','')
        
        timestamp = None
        if response.xpath("//time/@data-timestamp").get():
            timestamp_str = response.xpath("//time/@data-timestamp").get()
            timestamp = timestamp_str.replace('T',' ').replace('Z','')
        else:
            timestamp_str = response.xpath("//div[@class='source-and-publishdate-container']//span[@class='news-post-quotetime warmGrey']/text()").get()
            timestamp = datetime.strptime(timestamp_str, "%b. %d, %Y, %I:%M %p")
            
        article_dict['published_at'] = timestamp
        
        article_dict['link'] = response.url
        
        yield article_dict
    
    
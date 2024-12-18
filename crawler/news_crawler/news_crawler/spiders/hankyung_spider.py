import scrapy
from datetime import datetime
from news_crawler.news_crawler.user_agents import get_random_user_agent

class HankyungSpider(scrapy.Spider):
    name = 'hankyung' # Spider 이름 명시
    
    def __init__(self, latest_published_at: datetime, max_page: int = 200) -> None:
        self.latest_published_at = latest_published_at
        self.max_page = max_page
    
    def start_requests(self):
        # 20 articles per page
        yield scrapy.Request(
            url = "https://www.hankyung.com/koreamarket/news/all-news?page=1",
            headers = get_random_user_agent(),
            meta = {"page" : 1}
        )
            
    # 각 뉴스 목록 페이지에 있는 뉴스 기사 링크들을 가져온다.
    # 그 다음 가져온 링크들을 크롤링할 수 있는 parse_article 함수를 호출한다.
    def parse(self, response):
        stop_crawl_flag = False
        articles = articles = response.css("ul.news-list li div.news-item")
        for article in articles:
            article_date_str = article.css('p.txt-date::text').get()
            article_date = datetime.strptime(article_date_str, "%Y.%m.%d %H:%M")
            
            if self.latest_published_at and self.latest_published_at > article_date:
                stop_crawl_flag = True
                
            article_link = article.css('h2.news-tit > a::attr(href)').get()
            yield response.follow(
                url=article_link, 
                headers=get_random_user_agent(), 
                callback=self.parse_article
            )
            
        current_page = response.meta["page"]
        if not stop_crawl_flag and current_page < self.max_page:
            next_page = current_page + 1
            yield scrapy.Request(
                url = f"https://www.hankyung.com/koreamarket/news/all-news?page={next_page}",
                headers = get_random_user_agent(),
                callback = self.parse,
                meta = {"page" : next_page}
            )
            
    # 각 뉴스 기사 페이지를 크롤링한다
    def parse_article(self, response):
        # 뉴스 기사 정보를 dict 형태로 저장한다
        article_dict = {}
        article_dict['country'] = 'KOR'
        article_dict['title'] = response.xpath("normalize-space(//h1[@class='headline']/text())").get()
        
        img_ret = response.xpath("//div[@class='figure-img']/img/@src").get()
        article_dict['image_link'] =  img_ret if img_ret is not None else ''
        
        article_dict['source'] ='한국경제'
        article_dict['content'] = response.xpath("normalize-space(//div[@class='article-body'])").get()
        article_dict['published_at'] = response.xpath("//span[@class='txt-date']/text()").get().replace('.','-')
        article_dict['link'] = response.url
        
        yield article_dict
    




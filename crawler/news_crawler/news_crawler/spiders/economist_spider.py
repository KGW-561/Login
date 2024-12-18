import json
import scrapy
from datetime import datetime
from news_crawler.news_crawler.user_agents import get_random_user_agent

# 이코노미스트 사이트 크롤러
class EconomistSpider(scrapy.Spider):
    name = 'economist' # 이름 명시 (CLI로 크롤러를 호출할 때 필수)
    
    def __init__(self, latest_published_at: datetime, max_page: int = 200) -> None:
        self.latest_published_at = latest_published_at
        self.max_page = max_page
    
    # 서버에 GET 요청
    def start_requests(self):
        # 10 articles per page
        yield scrapy.Request(
            url = "https://economist.co.kr/article/items/ecn_SC001001000?returnType=ajax&page=1",
            headers = get_random_user_agent(),
            meta = {"page" : 1}
        )
        
            
    # 서버에서 받은 응답을 JSON으로 변환
    # 각 뉴스 목록 페이지에 있는 모든 기사를 가져오며 각 뉴스 기사의 정보를 dict 형태로 저장
    def parse(self, response):
        stop_crawl_flag = False
        
        response_json = json.loads(response.body)
        articles = response_json['result']['items']
        
        for article in articles:
            article_dict = {}
            article_dict['country'] = 'KOR'    
            article_dict['title'] = article['title']
            
            # 이미지가 없는 뉴스 기사도 있어서 try catch로 처리
            try:
                article_dict['image_link'] = article['files'][0]['path']
            except IndexError:
                article_dict['image_link'] = ''
                
            article_dict['source'] = '이코노미스트'
            article_dict['content'] = article['content'].replace("rdquo", '"').replace("ldquo", '"')
            article_dict['published_at'] = article['firstPublishDate']
            article_dict['link'] = 'https://economist.co.kr/article/view/' + article['aid']
            
            # 만약에 뉴스 기사 목록 페이지에 self.latest_published_at 보다 더 이른 날짜가 있다면 다음 페이지로 넘어가지 않는다.
            published_date = datetime.strptime(article['firstPublishDate'], "%Y-%m-%d %H:%M:%S")
            if self.latest_published_at and self.latest_published_at > published_date:
                stop_crawl_flag = True
            
            yield article_dict
            
        # stop_crawl_flag가 계속 False라면 다음 페이지로 넘어간다
        current_page = response.meta["page"]
        if not stop_crawl_flag and current_page < self.max_page:
            next_page = current_page + 1
            yield scrapy.Request(
                url = f"https://economist.co.kr/article/items/ecn_SC001001000?returnType=ajax&page={next_page}",
                headers = get_random_user_agent(),
                callback = self.parse,
                meta = {"page" : 2}
            )
            
    
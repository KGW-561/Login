import scrapy
from datetime import datetime
from news_crawler.news_crawler.user_agents import get_random_user_agent


class MaeilSpider(scrapy.Spider):
    name = "maeil"

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9,ko;q=0.8,fr;q=0.7",
        "Connection": "keep-alive",
        "DNT": "1",
        "Host": "www.mk.co.kr",
        "Referer": "https://www.mk.co.kr/news/business/latest/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": get_random_user_agent()["User-Agent"],
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
    }

    cookies = {
        "PCID": "17302645381415665605320",
        "SCOUTER": "z46vklbeoaffpv",
        "_sas_id.01.646b": "e307cdb4cb517f86.1730264538.",
        "MK_total_search_history": "%5B%22%ED%98%84%EB%8C%80%EC%B0%A8%22%5D",
        "_sas_ses.01.646b": "1",
    }

    def __init__(self, latest_published_at: datetime, max_page: int = 99) -> None:
        self.latest_published_at = latest_published_at
        self.max_page = max_page

    # 10 articles per page
    def start_requests(self):
        yield scrapy.Request(
            url="https://www.mk.co.kr/_CP/42?page=1&lang=null&lcode=business&scode=latest&date=null&category=null&mediaCode=null&sort=null&userNo=null&ga_category=data-category_1depth%3D%7C%EB%89%B4%EC%8A%A4%7C%20data-category_2depth%3D%7C%EA%B8%B0%EC%97%85%7C%20data-category_3depth%3D%7C%EC%B5%9C%EC%8B%A0%EB%89%B4%EC%8A%A4%7C%20%20data-section%3D%7C%EC%B5%9C%EC%8B%A0%EA%B8%B0%EC%82%AC%7C",
            headers=self.headers,
            cookies=self.cookies,
            meta = {"page" : 1}
        )

    def parse(self, response):
        stop_crawl_flag = False
        articles = response.xpath("//li[@class='news_node']")
        for article in articles:
            article_date_str = article.xpath(".//p[@class='time_info']/text()").get()
            article_date = datetime.strptime(article_date_str, "%Y-%m-%d %H:%M:%S")
            
            if self.latest_published_at and self.latest_published_at > article_date:
                stop_crawl_flag = True
            
            article_link = article.xpath("./a[@class='news_item']/@href").get()
            yield response.follow(
                url = article_link,
                headers = get_random_user_agent(),
                callback = self.parse_article
            )
            
        current_page = response.meta["page"]    
        if not stop_crawl_flag and current_page < self.max_page:
            next_page = current_page + 1
            
            yield scrapy.Request(
                url = f"https://www.mk.co.kr/_CP/42?page={next_page}&lang=null&lcode=business&scode=latest&date=null&category=null&mediaCode=null&sort=null&userNo=null&ga_category=data-category_1depth%3D%7C%EB%89%B4%EC%8A%A4%7C%20data-category_2depth%3D%7C%EA%B8%B0%EC%97%85%7C%20data-category_3depth%3D%7C%EC%B5%9C%EC%8B%A0%EB%89%B4%EC%8A%A4%7C%20%20data-section%3D%7C%EC%B5%9C%EC%8B%A0%EA%B8%B0%EC%82%AC%7C",
                headers = self.headers,
                cookies = self.cookies,
                callback = self.parse,
                meta = {"page" : next_page}
            )

    def parse_article(self, response):
        article_dict = {}

        article_dict["country"] = "KOR"
        article_dict["title"] = response.xpath("normalize-space(//h2[@class='news_ttl'])").get()
        article_dict["source"] = "매일경제"
        article_dict["image_link"] = response.xpath("//div[@class='thumb']/img/@src").get()

        content_str = "".join(response.xpath("//div[@itemprop='articleBody']/p/text()").getall())
        if content_str == "":
            article_dict["content"] = "".join(response.xpath("//div[@itemprop='articleBody']/text()").getall())
        else:
            article_dict["content"] = content_str

        article_dict['published_at'] = response.xpath("//*[@class='registration']/*[2]/text()").get()
        article_dict["link"] = response.url

        yield article_dict

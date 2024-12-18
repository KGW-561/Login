import re
import json
import scrapy
from scrapy import Request
from datetime import datetime
from parsel import Selector
from collections.abc import Iterable
from news_crawler.news_crawler.user_agents import get_random_user_agent

class MotelyFoolSpider(scrapy.Spider):
    name = 'motelyfool'
    
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9,ko;q=0.8,fr;q=0.7",
        "Dnt": "1",
        "Priority": "u=1, i",
        "Referer": "https://www.fool.com/market-trends/",
        "Sec-Ch-Ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "Sec-Ch-Ua-Mobile": "?1",
        "Sec-Ch-Ua-Platform": "\"Android\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        # "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
        "User-Agent": get_random_user_agent()['User-Agent'],
        "X-Requested-With": "fetch"
    }

    cookies = {
        "sessionid": "na8dy3c3lr6hpqhhs6oczw0fjtsd4ela",
        "Visit": "visit=a675afd3-502e-4109-ac8a-c7ad9cb3da51&first_article_in_session=0&first_marketing_page=0",
        "Visitor": "uid=&username=&account=&registered=false&ecapped=false&dskPrf=false&version=7&visits=1&visitor=cf098a45-a09b-4501-a89b-738905e80254",
        "OptanonAlertBoxClosed": "2024-12-01T23:15:55.624Z",
        "eupubconsent-v2": "CQI75RgQI75RgAcABBENBSFgAAAAAAAAACiQKqNX_G__bWlr8X73aftkeY1P9_h77sQxBhfJE-4FzLvW_JwXx2ExNA36tqIKmRIAu3TBIQNlGJDURVCgaogVryDMaEyUoTNKJ6BkiFMRM2dYCFxvm4tj-QCY5vr991dx2B-t7dr83dzyy4xHn3a5_2S0WJCdA5-tDfv9bROb-9IOd_x8v4v4_F_pE2_eT1l_tWvp7D9-cts__XW99_fff_9Pn_-uB_-_3_vf_EAAAAAA.YAAAAAAAAAAA",
        "infotron_popup_status": "dismissed",
        "InfoTrackClickImpression": "f2f8fec2-fc9b-4250-9bd9-e55db945a94f",
        "ajs_anonymous_id": "d8a03973-1060-43fb-bf90-084a949f43a9",
        "Sookie": "source=isaeditn0000028&ybls=0",
        "mms_sessionid": "is4ri908r9qku3d6w72rfktfenun4tnx",
        "OptanonConsent": "isGpcEnabled=0&datestamp=Mon+Dec+02+2024+09%3A20%3A59+GMT%2B0900+(Korean+Standard+Time)&version=202408.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=b69326c5-5c2b-4a5b-8319-525cf80b530c&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&AwaitingReconsent=false&groups=C0002%3A0%2CC0004%3A0%2CC0003%3A0%2CC0001%3A1%2CV2STACK42%3A0&intType=3&geolocation=KR%3B26",
        "cf_clearance": "vLtD0ptC9V_bAIm2_aZKjDg6MoC6n.GiRW3fpKHanqs-1733098860-1.2.1.1-L0E5zsnR.D3yIO2UZX2Uz2dU4SxVKxIwfd7m7KnuQIgypiQtcm28VZdZvk729zNEBGI1tCNCF2a2I5hbSG1D2NPKwrwyECT0Xm5SVpxG.C1OEvSexv5eo3kl.zl1uZOgnwbWJCy1IO_LsOjAz9h9Q3olpKhzv1ARyLmSfgYVLyDNyK7ae89ZEtOxTdM5m2lHxcQuTYWx9CTUPRlV8YylqdvHa0LiZVwXEUi7gBAqip8LrZqxfJ63ERPRsaclE9EU3gX2ODO5EXDdqMc7SXzIrQMKWZeVjZbgACvH8bDIia6NLpdhtKEvO1u1Ydd8sKMNGdrBTcbjLCeyENO4_9.mbnkxSNudvN33pyxIp2zfD2E2xnmtigCrgf3M83zqtdLy7.3ze3kO2eM0dBu7xfLTMslhPAqddHISvMBBK.J_KWw"
    }
    
    def __init__(self, latest_published_at: datetime, max_page: int = 200):
        self.latest_published_at = latest_published_at.replace(hour=0, minute=0, second=0, microsecond=0)
        self.max_page = max_page
    
    def start_requests(self) -> Iterable[Request]:
        yield scrapy.Request(
            url = "https://www.fool.com/market-trends/filtered_articles_by_page/?page=1",
            headers = self.headers,
            cookies = self.cookies,
            meta = {"page" : 1}
        )
    
    def parse(self, response):
        stop_crawl_flag = False
        response_json = json.loads(response.body)
        selector = Selector(text = response_json['html'])
        
        articles = selector.xpath("//div[@class='flex py-12px text-gray-1100']")
        for article in articles:
            article_date_str = article.xpath("normalize-space(.//div[@class='text-sm text-gray-800 mb-2px md:mb-8px']/text())").get().replace(" by", "").strip()
            article_date = datetime.strptime(article_date_str, "%b %d, %Y")
            
            if self.latest_published_at and self.latest_published_at > article_date:
                stop_crawl_flag = True
                
            article_link = article.xpath("./a[@class='flex-shrink-0 w-1/3 mr-16px sm:w-auto']/@href").get()
            yield response.follow(
                url = "https://www.fool.com" + article_link,
                headers = self.headers,
                cookies = self.cookies,
                callback = self.parse_article
            )
            
        current_page = response.meta["page"]
        if not stop_crawl_flag and current_page < self.max_page:
            next_page = current_page + 1
            yield scrapy.Request(
                url = f"https://www.fool.com/market-trends/filtered_articles_by_page/?page={next_page}",
                headers = self.headers,
                cookies = self.cookies,
                callback = self.parse,
                meta = {"page" : next_page}
            )
        
    def parse_article(self, response):
        article_dict = {}
        
        article_dict['country'] = 'USA'
        article_dict['title'] = response.xpath("//header/h1[@class='text-3xl font-medium tracking-tight text-gray-1100 leading-relative-2 md:text-5xl']/text()").get()
        article_dict['image_link'] = response.xpath("//div[@class='article-body']/div[@class='image']/img/@src").get()
        article_dict['source'] = 'The Motley Fool'
        article_dict['content'] = ''.join(response.xpath("//div[@class='article-body']//h2//text() | //div[@class='article-body']//p//text()").getall())
        
        datetime_str = response.xpath("normalize-space(//div[@class='content-container']/section[@class='bg-gray-100 pt-28px px-24px md:px-40px']/div[@class='md:grid md:gap-32px md:grid-flow-col foolcom-grid-content-sidebar mx-auto md:max-w-880 lg:max-w-1280 xl:gap-80 pb-24px md:pb-32px']/div/div)").get()
        article_dict['published_at'] = self.convert_datetime(datetime_str)
        article_dict['link'] = response.url
        
        yield article_dict
        
    def convert_datetime(self, input_string) -> str:
        cleaned_string = re.sub(r'\s+', ' ', input_string.strip())
        date_time_str = re.search(r'(\w+\s\d{1,2},\s\d{4}\sat\s\d{1,2}:\d{2}[APM]+)', cleaned_string).group(1)
        date_time_obj = datetime.strptime(date_time_str, '%b %d, %Y at %I:%M%p')
        formatted_date_time = date_time_obj.strftime('%Y-%m-%d %H:%M:%S')
        return formatted_date_time

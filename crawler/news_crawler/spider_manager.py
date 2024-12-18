# 한국 뉴스 크롤러
from news_crawler.news_crawler.spiders.economist_spider import EconomistSpider
from news_crawler.news_crawler.spiders.hankyung_spider import HankyungSpider
from news_crawler.news_crawler.spiders.maeil_spider import MaeilSpider

# 미국 뉴스 크롤러
from news_crawler.news_crawler.spiders.businessinsider_spider import BusinessInsiderSpider
from news_crawler.news_crawler.spiders.motleyfool_spider import MotelyFoolSpider
from news_crawler.news_crawler.spiders.zacks_spider import ZacksSpider

from repositories.crawler_repository import CrawlerRepository
from scrapy.crawler import CrawlerProcess
from typing import Dict
from datetime import datetime


class SpiderManager:

    crawler_settings = {
        "ROBOTSTXT_OBEY": False,
        "DOWNLOAD_DELAY": 1.5,
        "RANDOMIZE_DOWNLOAD_DELAY": True,
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_START_DELAY": 1,
        "AUTOTHROTTLE_MAX_DELAY": 8,
        "AUTOTHROTTLE_TARGET_CONCURRENCY": 1.0,
        "AUTOTHROTTLE_DEBUG": True,
        "ITEM_PIPELINES": {
            "news_crawler.news_crawler.pipelines.NewsCrawlerPipeline": 300
        },
    }

    def __init__(self):
        self.process = CrawlerProcess(self.crawler_settings)
        self.repository = CrawlerRepository()
        
    def get_latest_published_dates(self) -> Dict[str, datetime]:
        latest_published_dates = self.repository.get_latest_published_dates_by_website()        
        result = {key: value for publish_date in latest_published_dates for key, value in publish_date.items()}
        return result
        
    def run_spiders(self):
        latest_published_at = self.get_latest_published_dates()
        
        self.process.crawl(MaeilSpider, latest_published_at.get('매일경제'))
        self.process.crawl(HankyungSpider, latest_published_at.get('한국경제'))
        self.process.crawl(EconomistSpider, latest_published_at.get('이코노미스트'))

        self.process.crawl(BusinessInsiderSpider, latest_published_at.get('Business Insider'))
        self.process.crawl(MotelyFoolSpider, latest_published_at.get('The Motley Fool'))
        self.process.crawl(ZacksSpider, latest_published_at.get('Zack\'s'))
        
    def get_crawler_process(self) -> CrawlerProcess:
        return self.process
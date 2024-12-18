import re
from html import unescape

# import os
# import sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from repositories.crawler_repository import CrawlerRepository
from logs.logger import Logger


class NewsCrawlerPipeline:

    def __init__(self) -> None:
        self.logger = Logger(self.__class__.__name__)

    # 크롤러 생성 시 데이터베이스 연결
    def open_spider(self, spider) -> None:
        spider.repo = CrawlerRepository()
        spider.repo.connect()

    # 크롤러 소멸 시 데이터베이스 연결 끊기
    def close_spider(self, spider) -> None:
        if hasattr(spider, "repo"):
            spider.repo.disconnect()

    # 텍스트 전처리
    def sanitize(self, text: str) -> str:
        text = unescape(text)
        text = re.sub(r"사진=[^\s]*\s", "", text)  # 사진= 으로 시작하는 텍스트 제거
        text = re.sub(
            r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "", text
        )  # 이메일 제거
        text = re.sub(r"http[s]?://[^\s]+", "", text)  # URL 제거
        # text = re.sub(r"[^a-zA-Z가-힣0-9.,?!&^-\s]", "", text) # 한글, 영어, 숫자, 기본 문자(.,?!)를 제외한 모든 문자 제거
        text = re.sub(r"\s+", " ", text).strip()  # 긴 공백 문자 제거
        return text

    # 크롤링한 뉴스 기사를
    def process_item(self, item, spider):
        self.logger.log_info("Inserting item into database.")
        self.logger.log_info(f"Item: {str(item)}")
        self.logger.log_info(f"Spider: {str(spider)}")

        item["content"] = self.sanitize(item["content"])

        if hasattr(spider, "repo"):
            spider.repo.save_crawled_articles(item)
            spider.repo.create_log()

        return item

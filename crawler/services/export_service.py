from services.base_service import BaseService
from repositories.export_repository import ExportRepository
from models.news_process_log import NewsProcessLog
from models.article import Article
from logs.logger import Logger
from enums.status import Status
from enums.log_msg import LogMsg
from typing import List


class ExportService(BaseService):

    def __init__(self):
        self.logger = Logger(self.__class__.__name__)
        self.repository = ExportRepository()

    # 텍스트 가공한 뉴스 기사들을 해당하는 데이터베이스 테이블로 삽입
    def process(self) -> List[NewsProcessLog]:
        self.logger.log_info("Exporting articles to corresponding tables.")

        # 가공된 기사들
        articles: list[Article] = self.repository.fetch_processed_data()

        # 가공 로그
        process_logs = []

        kor_econ_news = []  # 한국 경제 뉴스
        usa_econ_news = []  # 미국 경제 뉴스
        kor_stock_news = []  # 한국 주식 뉴스
        usa_stock_news = []  # 미국 주식 뉴스
        
        # Article 객체의 news_type과 country에 따라 분류
        # 한국 경제 뉴스, 한국 주식 뉴스, 미국 경제 뉴스, 미국 주식 뉴스
        for article in articles:
            if article.news_type == "economy":
                if article.country == "KOR":
                    kor_econ_news.append(article)
                elif article.country == "USA":
                    usa_econ_news.append(article)

            elif article.news_type == "stock":
                if article.country == "KOR":
                    kor_stock_news.append(article)
                elif article.country == "USA":
                    usa_stock_news.append(article)

            # 가공 로그에 뉴스 기사 id, 작업 상태 (status), 로그 메세지 (log_msg) 생성
            process_logs.append(
                NewsProcessLog(
                    raw_news_id=article.raw_news_id,
                    status=Status.SUCCESS.value,
                    log_msg=LogMsg.PROCESS_COMPLETED.value,
                )
            )

        # 해당하는 테이블에 뉴스 기사들을 삽입한다
        if kor_econ_news:
            self.repository.insert_econ_news(country="KOR", econ_articles=kor_econ_news)
        if usa_econ_news:
            self.repository.insert_econ_news(country="USA", econ_articles=usa_econ_news)
        if kor_stock_news:
            self.repository.insert_stock_news(country="KOR", stock_articles=kor_stock_news)
        if usa_stock_news:
            self.repository.insert_stock_news(country="USA", stock_articles=usa_stock_news)

        return process_logs  # 가공 로그를 ProcessManager에 반환

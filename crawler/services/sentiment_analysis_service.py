from services.base_service import BaseService
from repositories.sentiment_analyzer_repository import SentimentAnalyzerRepository
from processors.sentiment_analyzer import SentimentAnalyzer
from models.news_process_log import NewsProcessLog
from models.article import Article
from logs.logger import Logger
from enums.status import Status
from typing import List


class SentimentAnalysisService(BaseService):

    def __init__(self):
        self.logger = Logger(self.__class__.__name__)
        self.processor = SentimentAnalyzer()
        self.repository = SentimentAnalyzerRepository()

    # 감정평가 작업
    def process(self) -> List[NewsProcessLog]:
        self.logger.log_info("Analyzing sentiment from articles.")

        # 데이터베이스에서 아직 감정 평가 안된 기사들을 가져오기
        articles: list[Article] = self.repository.fetch_unprocessed_data()

        process_logs = []  # 가공 로그
        sentiment_analyzed_articles = []  # 감정평가
        for article in articles:
            result = self.processor.analyze(article)

            if result.get("status") == Status.SUCCESS.value:
                article.sentiment = result.get("sentiment")
                sentiment_analyzed_articles.append(article)

            process_logs.append(
                NewsProcessLog(
                    raw_news_id=article.raw_news_id,
                    status=result.get("status"),
                    log_msg=result.get("log_msg"),
                )
            )

        if sentiment_analyzed_articles:
            self.repository.save_processed_data(sentiment_analyzed_articles)

        return process_logs

from news_crawler.spider_manager import SpiderManager
from services.translation_service import TranslationService
from services.keyword_extraction_service import KeywordExtractionService
from services.sentiment_analysis_service import SentimentAnalysisService
from repositories.news_process_log_repository import NewsProcessLogRepository
from services.export_service import ExportService
from enums.process import Process
from logs.logger import Logger
from scrapy.crawler import CrawlerProcess

# 작업 Controller
class NewsProcessManager:

    def __init__(self) -> None:
        self.logger = Logger(self.__class__.__name__)
        self.log_repo = NewsProcessLogRepository()
        self.spider_manager = SpiderManager()
        
    # 크롤러 호출
    def crawl(self) -> None:
        self.logger.log_info("Crawling articles from the web.")
        # spider_manager = SpiderManager()
        # spider_manager.run_spiders()
        self.spider_manager.run_spiders()
        
    def get_crawler_process(self) -> CrawlerProcess:
        return self.spider_manager.get_crawler_process()

    # Papago API로 영문 기사 한국어로 번역
    def translate(self) -> None:
        translation_service = TranslationService()
        process_logs = translation_service.process()

        self.log_repo.update_logs(process=Process.TRANSLATION, logs=process_logs)

    # 키워드 추출
    def extract_keywords(self) -> None:
        keyword_service = KeywordExtractionService()
        process_logs = keyword_service.process()

        self.log_repo.update_logs(process=Process.KEYWORD_EXTRACTION, logs=process_logs)

    # Clova Studio API로 감정평가 작업
    def analyze_sentiment(self) -> None:
        sentiment_service = SentimentAnalysisService()
        process_logs = sentiment_service.process()

        self.log_repo.update_logs(process=Process.SENTIMENT_ANALYSIS, logs=process_logs)

    # 모든 작업이 끝난 기사를 뉴스 기사 테이블들로 삽입
    # kor_econ_news, kor_stock_news, usa_econ_news, usa_stock_news
    def export(self) -> None:
        export_service = ExportService()
        process_logs = export_service.process()
        self.log_repo.update_logs(process=Process.COMPLETED, logs=process_logs)

    # 모든 작업 실행
    def run(self) -> None:
        print("RUNNING!")
        self.crawl()
        self.translate()
        self.extract_keywords()
        self.analyze_sentiment()
        self.export()
from services.base_service import BaseService
from processors.keyword_extractor import KeywordExtractor
from repositories.keyword_extractor_respository import KeywordExtractorRepository
from repositories.ticker_repository import TickerRepository
from models.news_process_log import NewsProcessLog
from models.article import Article
from logs.logger import Logger
from typing import List


class KeywordExtractionService(BaseService):

    def __init__(self) -> None:
        self.logger = Logger(self.__class__.__name__)
        self.repository = KeywordExtractorRepository()
        self.processor = KeywordExtractor()

    # 키워드 추출 작업
    def process(self) -> List[NewsProcessLog]:
        self.logger.log_info("Extracting keyword from articles.")

        # 키워드 티커 정보를 KeywordExtractor에 주입
        ticker_repository = TickerRepository()
        ticker_dict = ticker_repository.fetch_ticker_dict() # 데이터베이스에서 주식 티커 정보 가져오기
        self.processor.get_tickers(ticker_dict)

        # 데이터베이스에서 아직 키우드 추출 안된 기사들을 가져오기
        articles: list[Article] = (self.repository.fetch_unprocessed_data())  # Article 객체 배열
        

        process_logs = [] # 키워드 추출 로그들
        extracted_articles = [] # 키워드 추출된 뉴스 기사들

        for article in articles:
            result = self.processor.extract(article)

            # 키워드 추출은 API에 의존하지 않기 때문에 Status 여부는 모두 성공(SUCCESS)이다
            news_type = result.get("news_type")
            companies = result.get("companies")

            # 뉴스 기사 하나가 여러 주식 종목에 대해 보도할 수 있기 때문에 
            # 추출된 주식 종목만큼 Article 객체를 생성한다
            if news_type == "stock":
                ticker_ids = [ticker_dict.get(company) for company in companies]
                
                # 새로 생성된 주식 종목 기사들을 리스트에 저장
                extracted_articles.extend(
                    Article(
                        raw_news_id=article.raw_news_id,
                        news_type=news_type,
                        ticker_id=ticker_id,
                    )
                    for ticker_id in ticker_ids
                )

            # 경제 뉴스 기사라면 추출할 주식 종목이 없기에 news_type만 지정하고 리스트에 저장
            else:
                article.news_type = news_type
                extracted_articles.append(article)

            # 가공 로그에 뉴스 기사 id, 작업 상태 (status), 로그 메세지 (log_msg) 생성
            process_logs.append(
                NewsProcessLog(
                    raw_news_id=article.raw_news_id,
                    status=result.get("status"),
                    log_msg=result.get("log_msg"),
                )
            )

        # 키워드 추출된 기사들을 테이블에 저장
        if extracted_articles:
            self.repository.save_processed_data(extracted_articles)

        return process_logs

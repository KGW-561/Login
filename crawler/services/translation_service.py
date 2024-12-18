from services.base_service import BaseService
from repositories.translator_repository import TranslatorRepository
from processors.papago_translator import PapagoTranslator
from models.news_process_log import NewsProcessLog
from models.article import Article
from enums.status import Status
from logs.logger import Logger
from typing import List


class TranslationService(BaseService):

    def __init__(self):
        self.logger = Logger(self.__class__.__name__)
        self.processor = PapagoTranslator()
        self.repository = TranslatorRepository()

    def process(self) -> List[NewsProcessLog]:
        self.logger.log_info("Translating articles from English to Korean.")

        translator = PapagoTranslator()
        translator_repo = TranslatorRepository()

        # 데이터베이스에서 아직 번역 안된 기사들을 가져오기
        articles: list[Article] = translator_repo.fetch_unprocessed_data()

        process_logs = []
        translated_articles = []
        # 번역 작업 실행
        for article in articles:
            # 번역 결과를 dict로 받음
            result = translator.translate(article)  # dict[str, str]

            # 번역 작업에 성공했다면 결과 리스트에 넣음
            if result.get("status") == Status.SUCCESS.value:
                article.title = result.get("title")
                article.content = result.get("content")

                translated_articles.append(article)

            # 작업 로그 넣음
            process_logs.append(
                NewsProcessLog(
                    raw_news_id=article.raw_news_id,
                    status=result.get("status"),
                    log_msg=result.get("log_msg"),
                )
            )

        if translated_articles:
            translator_repo.save_processed_data(translated_articles)

        return process_logs

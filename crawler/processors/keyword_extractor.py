import re
import json
from typing import Dict

from models.article import Article
from enums.status import Status
from enums.log_msg import LogMsg
from logs.logger import Logger


class KeywordExtractor:

    def __init__(self) -> None:
        self.logger = Logger(self.__class__.__name__)

    def get_tickers(self, ticker_dict: Dict[str, str]) -> None:
        self.ticker_dict = ticker_dict

    # 뉴스 기사에 최대한 기업명만 남기기 위한 텍스트 가공
    def remove_noise(self, article) -> str:
        # 한국어 조사 필터링
        result = re.sub(r"(와|과|은|는|이|가|을|를|에|의|로|으로|도|만|까지|부터|밖에)\b"," ", article)  
        result = re.sub(r"(^[^가-힣a-zA-Z]+|[^가-힣a-zA-Z]+$)", "", result)  # 단어 시작과 끝에 있는 특수 문자 필터링
        result = result.replace("네이버", "NAVER")  # 네이버는 NAVER로 switch함
        result = result.replace("(", " ").replace(")", " ")

        return result

    # 키워드 추출
    def extract(self, article: Article) -> dict:
        if not self.ticker_dict:
            self.logger.log_error("Ticker dict is not set for KeywordExtractor.")
            return None

        cleaned_article = self.remove_noise(article.content)
        # 뉴스 기사를 리스트로 변형해서 키워드 추출
        mentioned_companies = set(cleaned_article.split(" ")).intersection(
            set(self.ticker_dict.keys())
        )

        result = None
        # 회사명(KOSPI 200, S&P 500)이 기사에 있을 때
        if mentioned_companies:
            result = {
                "status": Status.SUCCESS.value,
                "log_msg": LogMsg.KEYWORD_EXTRACTION_SUCCESS.value,
                "news_type": "stock",
                "companies": list(mentioned_companies),
            }
        else:
            # 키워드 추출한 API 호출이 아닌 rule-based라서 실패하는 케이스 없음
            result = {
                "status": Status.SUCCESS.value,
                "log_msg": LogMsg.KEYWORD_EXTRACTION_SUCCESS.value,
                "news_type": "economy",
                "companies": None,
            }

        return result

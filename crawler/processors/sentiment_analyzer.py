import os
import requests
import json
from json.decoder import JSONDecodeError
from time import sleep
from dotenv import load_dotenv
from typing import Dict

from models.article import Article
from enums.status import Status
from enums.log_msg import LogMsg
from logs.logger import Logger


class SentimentAnalyzer:

    # env 파일에서 환경 변수를 가져온다
    def __init__(self) -> None:
        load_dotenv()
        self.host = os.getenv("CLOVA_HOST")
        self.api_key = os.getenv("CLOVA_SENTIMENT_API_KEY")
        self.api_key_primary_val = os.getenv("CLOVA_SENTIMENT_PRIMARY_VAL")
        self.request_id = os.getenv("CLOVA_SENTIMENT_REQUEST_ID")
        self.logger = Logger(self.__class__.__name__)

    # Clova Studio API 요청을 위한 header 반환
    def get_headers(self) -> Dict[str, str]:
        return {
            "X-NCP-CLOVASTUDIO-API-KEY": self.api_key,
            "X-NCP-APIGW-API-KEY": self.api_key_primary_val,
            "X-NCP-CLOVASTUDIO-REQUEST-ID": self.request_id,
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "text/event-stream",
        }

    # Clova Studio API 요청에 필요한 payload 반환
    def get_request_data(self, text: str) -> Dict:

        prompt = """
        다음은 뉴스 기사입니다. 기사의 전반적인 감정(긍정적, 부정적, 중립적)을 분석하고, 결과만 출력하세요.
        \n결과는 다음 JSON 형식으로 작성하세요:

        { "sentiment" : "positive" / "negative" / "neutral"}
        
        다음은 분석해야 할 뉴스 기사입니다:
        """

        preset_text = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": text},
        ]

        return {
            "messages": preset_text,
            "topP": 0.8,
            "topK": 0,
            "maxTokens": 150,
            "temperature": 0.03,
            "repeatPenalty": 1.2,
            "stopBefore": [],
            "includeAiFilters": False,
            "seed": 0,
        }

    # Clova Studio API에서 받은 응답을 json으로 변환해서 감정평가 결과를 가져온다
    # 프롬프트로 JSON 형식으로 출력하라고 요청했기 때문에 가능함
    def format_output(self, result_str: str) -> str:
        try:
            response_json = json.loads(result_str)
            content_json = json.loads(response_json["message"]["content"])
            sentiment = content_json["sentiment"]
            return sentiment
        except JSONDecodeError as je:
            # 만약에 Clova Studio API가 형식대로 답변을 안할 경우
            # 가끔식 형식을 벗어나는 답변을 하는 경우가 있음
            self.logger.log_error(f"Error decoding JSON: {je}")
            self.logger.log_error(f"API Result: {result_str}")
            if "positive" in result_str:
                return "positive"
            elif "negative" in result_str:
                return "negative"
            elif "neutral" in result_str:
                return "neutral"

            return None

    # API에서 에러가 날 경우 에러 코드와 메세지를 json으로 변환해서 포맷한다
    def format_error(self, error_str: str) -> list:
        response_json = json.loads(error_str)
        return [response_json["status"]["code"], response_json["status"]["message"]]

    # 감정 평가 작업
    def analyze(self, article: Article) -> dict[str, str]:
        content = article.content[:5000] # Text too long 에러를 막기 위해 강제 슬라이싱 
        
        headers = self.get_headers() # 요청 header
        request_data = self.get_request_data(content) # payload

        sleep(0.5)  # Too Many Requests 에러를 막기 위한 강제 sleep

        result = None
        with requests.post(self.host, headers=headers, json=request_data) as response:
            if response.status_code == 200: # 응답이 200 OK일 경우
                response_text = response.text.split("\n\n") # 응답을 긴 string 형식으로 받는다
                for text in response_text:
                    if "event:result" in text:
                        idx = text.find("data:")
                        result_str = text[idx + len("data:") :].strip()
                        sentiment = self.format_output(result_str)
                        
                        # 감정 평가 결과 값 JSON 형식을 따르지 않는 경우
                        # 가끔식 Clova Studio API가 형식을 따르지 않는 경우가 있음. 
                        if not sentiment:
                            failed_reason = (f"Clova Studio threw unexpected result: {result_str}")
                            result = {
                                "status": Status.FAILED.value,
                                "log_msg": LogMsg.SENTIMENT_ANALYSIS_FAILED.format_failed_msg(article_id=article.raw_news_id, reason=failed_reason),
                                "sentiment": sentiment,
                            }
                        else:
                            # 답변이 JSON 형태로 정상적일 시
                            result = {
                                "status": Status.SUCCESS.value,
                                "log_msg": LogMsg.SENTIMENT_ANALYSIS_SUCCESS.value,
                                "sentiment": sentiment,
                            }

                        self.logger.log_info(json.dumps(result, indent=2))

                        return result

                    # API에서 에러를 반환할 때
                    elif "event:error" in text:
                        idx = text.find("data:")
                        error_str = text[idx + len("data:") :].strip()
                        error_details = self.format_error(error_str)
                        failed_reason = ("Status: " + error_details[0] + "\n Reason: " + error_details[1]
                        )

                        result = {
                            "status": Status.FAILED.value,
                            "log_msg": LogMsg.SENTIMENT_ANALYSIS_FAILED.format_failed_msg(
                                article_id=article.raw_news_id, reason=failed_reason
                            ),
                            "sentiment": "",
                        }

                        self.logger.log_info(json.dumps(result, indent=2))

                        return result

            # 서버에서 요청이 실패할 시
            else:
                failed_reason = (
                    "Http Status: "
                    + str(response.status_code)
                    + "\nMessage: "
                    + response.text
                )

                result = {
                    "status": Status.FAILED.value,
                    "log_msg": LogMsg.SENTIMENT_ANALYSIS_FAILED.format_failed_msg(
                        article_id=article.raw_news_id, reason=failed_reason
                    ),
                    "sentiment": "",
                }

                self.logger.log_info(json.dumps(result, indent=2))

                return result

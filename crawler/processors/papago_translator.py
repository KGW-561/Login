import os
import requests
import json
import nltk
from dotenv import load_dotenv
from time import sleep
from nltk.tokenize import sent_tokenize 

from models.article import Article
from enums.status import Status
from enums.log_msg import LogMsg
from logs.logger import Logger
                
class PapagoTranslator:
    
    API_URL = 'https://naveropenapi.apigw.ntruss.com/nmt/v1/translation'
    MAX_TEXT_LENGTH = 4800
    
    # API에 필요한 환경 변수 설정
    def __init__(self) -> None:
        load_dotenv()
        self.client_id = os.getenv('PAPAGO_CLIENT_ID')
        self.client_secret = os.getenv('PAPAGO_CLIENT_SECRET')
        self.glossary_key = os.getenv('PAPAGO_GLOSSARY_KEY')
        self.logger = Logger(self.__class__.__name__)
        nltk.download('punkt')
        nltk.download('punkt_tab')
        
    # 번역할 변수 설정
    def get_payload(self, text: str) -> dict:
        return {
            'source': 'en', # 원본의 언어 - 영어
            'target': 'ko', # 번역할 언어 - 한국어
            'glossaryKey' : self.glossary_key, #용어집 ID
            'honorific' : 'true', # 높임말 - true
            'text': text # 번역할 텍스트
        }
    
    # API 호출에 필요한 client_id와 client_secret 설정
    def get_headers(self):
        return {
            "X-NCP-APIGW-API-KEY-ID": self.client_id,
            "X-NCP-APIGW-API-KEY": self.client_secret,
        }
        
    # Papago API의 불규칙한 결과값 때문에 제목이랑 내용을 따로 번역함
    def translate(self, article: Article) -> dict[str, str]:
        title_result = self.execute_request(article.title) # 기사 제목
        content_result = self.translate_content(article.content) # 기사 내용
        
        result = None
        # 번역 작업이 둘 다 성공했을 시 번역 성공
        if title_result.get('status') == Status.SUCCESS.value and content_result.get('status') == Status.SUCCESS.value:
            status = Status.SUCCESS.value
            log_msg = LogMsg.TRANSLATION_SUCCESS.value
            translated_title = title_result.get('text') # 번역된 제목
            translated_content = content_result.get('text') # 번역된 내용
            
            # 번역 작업 결과
            result = {
                'status' : status, # 작업 성공 여부
                'log_msg' : log_msg, # 로그 상태 메세지
                'title' : translated_title, # 번역된 제목
                'content' : translated_content # 번역된 내용
            }
            
        
        else:
            reason = '' # 실패한 이유
            
            # 제목, 내용이 실패하거나 둘 다 실패 했을 시
            if title_result.get('status') == Status.FAILED.value:
                reason += title_result.get('reason')
                
            if content_result.get('status') == Status.FAILED.value:
                reason += content_result.get('reason')
                
            status = Status.FAILED.value
            failed_reason = reason
            log_msg = LogMsg.TRANSLATION_FAILED.format_failed_msg(article_id = article.raw_news_id, reason = failed_reason)
            
            result = {
                'status' : status,
                'log_msg' : log_msg,
                'title' : '',
                'content' : ''
            }
            
        self.logger.log_info(f"Article #{article.raw_news_id}")
        self.logger.log_info(json.dumps(result, ensure_ascii=False))
        
        return result
        
    # 번역할 수 있는 최대 글자 수를 넘기면 NLTK 라이브러리로 문장 단위로 기사 내용을 나눈다.
    def chunk_text_by_sentence(self, text: str) -> list[str]:
        sentences = sent_tokenize(text)
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) + 1 <= self.MAX_TEXT_LENGTH:
                current_chunk += (sentence + " ")
            else:
                chunks.append(current_chunk.strip())
                current_chunk = sentence + " "
        
        # 남은 chunk를 리스트에 담음
        if current_chunk:  
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def translate_content(self, content: str) -> dict[str, str]:
        # 최대 글자 수를 넘으면 리스트로 기사 내용을 자름
        content_chunks = self.chunk_text_by_sentence(content) if len(content) > self.MAX_TEXT_LENGTH else [content]
        # 자른 기사 내용을 번역한다.
        translated_content = []
        for chunk in content_chunks:
            content_result = self.execute_request(chunk)
            if content_result.get('status') == Status.SUCCESS.value:
                translated_content.append(content_result.get('text'))
            else:
                return {
                    'status': Status.FAILED.value,
                    'reason': content_result.get('reason'),
                    'text' : '',
                }
        
        # 나눈 기사 내용을 다시 붙힘
        concatenated_translated_content = ''.join(translated_content)
            
        return {
            'status' : Status.SUCCESS.value,
            'reason' : '',
            'text' : concatenated_translated_content
        }
        
    # 영어에서 한국어로 번역
    def execute_request(self, text: str) -> dict[str, str]:    
        sleep(0.5)
        # POST로 API 호출
        payload = self.get_payload(text)
        headers = self.get_headers()
        response = requests.post(self.API_URL, headers=headers, data=payload)
        
        try:
            # 서버 응답 코드 확인
            if response.status_code == 200: # 200 OK
                response_json = response.json()
                translated_text = response_json['message']['result']['translatedText']
                return {
                    'status' : Status.SUCCESS.value,
                    'reason' : '',
                    'text' : translated_text
                }

            # 서버 요청이 실패할 시
            else:
                failed_reason = "Status Code: " + str(response.status_code) + "\nMessage: " + response.text + '. '
                return {
                    'status' : Status.FAILED.value,
                    'reason' : failed_reason,
                    'text' : ''
                }
        except requests.exceptions as req_e:
            self.logger.log_error("Error sending request to Papago API.")
            self.logger.log_error(req_e)
            
            return {
                'status' : Status.FAILED.value,
                'reason' : req_e,
                'text' : ''
            }
        
    

        

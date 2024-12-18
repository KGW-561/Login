import os
import json
import requests
import time
from datetime import datetime
from dotenv import load_dotenv
from logs.logger import Logger

class KisTokenManager:
    
    BASE_URL = "https://openapi.koreainvestment.com:9443"
    
    def __init__(self):
        load_dotenv()
        self.app_key = os.getenv("KIS_APP_KEY")
        self.app_secret = os.getenv("KIS_APP_SECRET")
        self.access_token = None
        self.access_token_expiration = None
        self.token_json = os.path.join(os.path.dirname(__file__), "../kis_token.json")
        self.logger = Logger(self.__class__.__name__)
        
    # kis_token.json 파일에서 토큰 정보를 가져온다
    # 파일이 없거나 토큰 정보를 가져오는데 에러가 있다면 False를 반환
    # 문제가 없다면 True를 반환
    def _load_token(self) -> bool:
        if not os.path.exists(self.token_json):
            self.logger.log_error("[kis_token.json] file does not exist.")
            self.logger.log_error("Please create a file named: kis_token.json")
            return False
        
        try:
            with open(self.token_json, "r") as file:
                data = json.load(file)
                # 토큰 정보를 json파일에서 읽는다
                token = data.get("access_token")
                expiration = data.get("token_expiration")
                if not token and not expiration:
                    return False
                
                # 토큰 정보를 객체 변수로 저장
                self.access_token = token
                self.access_token_expiration = expiration
                
            return True
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            self.logger.log_error(f"Error loading token: {e}")
            return False
        
    def _save_token(self) -> None:
        try:
            with open(self.token_json, "w") as file:
                json.dump({
                    "access_token": self.access_token,
                    "token_expiration": self.access_token_expiration
                }, file)
        except Exception as e:
            self.logger.log_error(f"Error saving token: {e}")
        
    # 한국투자증권 API에 토큰 발급 요청을 한다.
    def _request_access_token(self) -> None:
        request_link = f"{self.BASE_URL}/oauth2/tokenP"
        
        headers = {
            "content-type" : "application/json"
        }
        
        body = {
            "grant_type":"client_credentials",
            "appkey" : self.app_key, 
            "appsecret": self.app_secret
        }
        
        try:
            response = requests.post(url = request_link, headers = headers, data = json.dumps(body))    
            response.raise_for_status()

            response_json = response.json()
            access_token = response_json["access_token"]
            access_token_expiration = response_json["access_token_token_expired"]
            
            self.access_token = access_token
            self.access_token_expiration = access_token_expiration
        except requests.exceptions.RequestException as req_e:
            self.logger.log_error("Error requesting KIS Access Token.")
            self.logger.log_error(f"Http Status: {response.status_code}. Reason: {req_e}")
            
    def is_token_expired(self) -> bool:
        return datetime.now() >= datetime.strptime(self.access_token_expiration, "%Y-%m-%d %H:%M:%S")
    
    def get_token(self) -> str:
        if self._load_token() and not self.is_token_expired():
            return self.access_token
        
        self._request_access_token()
        self._save_token()
        return self.access_token
        
        
        
        
            
    
        
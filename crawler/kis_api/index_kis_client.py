import asyncio
import aiohttp
from aiolimiter import AsyncLimiter
from datetime import datetime
from typing import List, Dict

from kis_api.base_kis_client import BaseKisClient
from models.index import Index



class IndexKisClient(BaseKisClient):
    
    async def fetch_kor_index(self, indices: List[Dict]) -> List[Dict]:
        limiter = AsyncLimiter(max_rate=15, time_period=1)
        async with aiohttp.ClientSession() as session:
            tasks = []
            for index in indices:
                end_point = f"{self.DOMAIN_URL}/uapi/domestic-stock/v1/quotations/inquire-index-price"
                headers = {
                    "content-type": "application/json; charset=utf-8",
                    "authorization": f"Bearer {self.access_token}",
                    "appkey": self.app_key,
                    "appsecret": self.app_secret,
                    "tr_id": "FHPUP02100000",
                    "custtype": "P"
                }
                
                params = {
                    "FID_COND_MRKT_DIV_CODE": "U",
                    "FID_INPUT_ISCD": index.get("fid")
                }
                
                tasks.append(self.make_request(session=session, limiter=limiter, url=end_point, headers=headers, params=params, identifier=index.get("title")))
            kor_indices_data = await asyncio.gather(*tasks)
        return kor_indices_data    
        
    async def fetch_usa_index(self, indices: List[Dict]) -> List[Dict]:
        limiter = AsyncLimiter(max_rate=15, time_period=1)
        async with aiohttp.ClientSession() as session:
            tasks = []
            for index in indices:
                
                end_point = f"{self.DOMAIN_URL}/uapi/overseas-price/v1/quotations/inquire-daily-chartprice"
                today_date = datetime.now().strftime("%Y%m%d")
                headers = {
                    "content-type": "application/json",
                    "authorization": f"Bearer {self.access_token}",
                    "appkey": self.app_key,
                    "appsecret": self.app_secret,
                    "tr_id": "FHKST03030100"
                }
                params = {
                    "FID_COND_MRKT_DIV_CODE": "N",
                    "FID_INPUT_ISCD": index.get("iscd"),
                    "FID_INPUT_DATE_1": today_date,
                    "FID_INPUT_DATE_2": today_date,
                    "FID_PERIOD_DIV_CODE": "D"
                }
                tasks.append(self.make_request(session=session, limiter=limiter, url=end_point, headers=headers, params=params, identifier=index.get("title")))
            usa_indices_data = await asyncio.gather(*tasks)
        return usa_indices_data
        
            
    
            
        
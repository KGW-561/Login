import asyncio
import aiohttp
from aiolimiter import AsyncLimiter
from typing import List, Dict
from datetime import datetime
from kis_api.base_kis_client import BaseKisClient
from models.forex import Forex

class ForexKisClient(BaseKisClient):
    
    async def fetch_forex(self, forexes: List[Dict]) -> Forex:
        limiter = AsyncLimiter(max_rate=15, time_period=1)
        async with aiohttp.ClientSession() as session:
            tasks = []
            for forex in forexes:
                end_point = f"{self.DOMAIN_URL}/uapi/overseas-price/v1/quotations/inquire-daily-chartprice"
                today_date = datetime.now().strftime("%Y%m%d")
                headers = {
                    "content-type": "application/json; charset=utf-8",
                    "authorization": f"Bearer {self.access_token}",
                    "appkey": self.app_key,
                    "appsecret": self.app_secret,
                    "tr_id": "FHKST03030100"
                }
                params = {
                    "FID_COND_MRKT_DIV_CODE": "X",
                    "FID_INPUT_ISCD": forex.get("iscd"),
                    "FID_INPUT_DATE_1": today_date,
                    "FID_INPUT_DATE_2": today_date,
                    "FID_PERIOD_DIV_CODE": "D"
                }
                tasks.append(self.make_request(session=session, limiter=limiter, url=end_point, headers=headers, params=params, identifier=forex.get("title")))
            forexes_data = await asyncio.gather(*tasks)
        return forexes_data
    
    
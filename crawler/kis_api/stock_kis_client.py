import asyncio
import aiohttp
import json
from aiolimiter import AsyncLimiter
from kis_api.base_kis_client import BaseKisClient
from models.ticker import Ticker
from models.kor_stock import KORStock
from models.usa_stock import USAStock
from typing import List, Dict


class StockKisClient(BaseKisClient):
    
    async def fetch_kor_stock_quotes(self, kor_tickers: List[Ticker]) -> List[Dict]:
        limiter = AsyncLimiter(max_rate=15, time_period=1)
        async with aiohttp.ClientSession() as session:
            tasks = []
            
            for kor_ticker in kor_tickers:
                end_point = f"{self.DOMAIN_URL}/uapi/domestic-stock/v1/quotations/inquire-price-2"
                headers = {
                    "content-type": "application/json; charset=utf-8",
                    "authorization": f"Bearer {self.access_token}",
                    "appkey": self.app_key,
                    "appsecret": self.app_secret,
                    "tr_id": "FHPST01010000",
                    "custtype" : "P"
                }
                params = {
                    "fid_cond_mrkt_div_code" : "J",
                    "fid_input_iscd" : kor_ticker.symbol
                }
                
                tasks.append(self.make_request(session=session, limiter=limiter, url=end_point, headers=headers, params=params, identifier=kor_ticker.ticker_id))
            kor_quote_data = await asyncio.gather(*tasks)
        return kor_quote_data
            
    async def fetch_usa_stock_quotes(self, usa_tickers: List[Ticker]) -> USAStock:
        limiter = AsyncLimiter(max_rate=13, time_period=1)
        async with aiohttp.ClientSession() as session:
            tasks = []
            
            for usa_ticker in usa_tickers:
                end_point = f"{self.DOMAIN_URL}/uapi/overseas-price/v1/quotations/price-detail"
                headers = {
                    "content-type": "application/json; charset=utf-8",
                    "authorization": f"Bearer {self.access_token}",
                    "appkey": self.app_key,
                    "appsecret": self.app_secret,
                    "tr_id": "HHDFS76200200",
                }
                params = {
                    "AUTH" : "",
                    "EXCD" : usa_ticker.exchange[:3],
                    "SYMB" : usa_ticker.symbol
                }
                
                tasks.append(self.make_request(session=session, limiter=limiter, url=end_point, headers=headers, params=params, identifier=usa_ticker.ticker_id))
            usa_quote_data = await asyncio.gather(*tasks)
        return usa_quote_data
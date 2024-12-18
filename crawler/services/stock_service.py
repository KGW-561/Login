from yfinance_crawler.yfinance_client import YFinanceClient
from repositories.stock_repository import StockRepository
from repositories.ticker_repository import TickerRepository
from models.ticker import Ticker
from models.kor_stock import KORStock
from models.usa_stock import USAStock
from typing import List

class StockService:
    
    def __init__(self):
        self.yfinance_client = YFinanceClient()
        self.stock_repository = StockRepository()
        self.ticker_repository = TickerRepository()
    
    def get_kor_stock_info(self) -> None:
        kor_tickers: List[Ticker] = self.ticker_repository.fetch_kor_tickers()
        
        for kor_ticker in kor_tickers:
            kor_stock: KORStock = self.yfinance_client.get_stock_info(country = "KOR", ticker = kor_ticker)
            self.stock_repository.upsert_kor_stock(kor_stock)  
                    
    def get_usa_stock_info(self) -> None:
        usa_tickers: List[Ticker] = self.ticker_repository.fetch_usa_tickers()
        
        for usa_ticker in usa_tickers:
            usa_stock: USAStock = self.yfinance_client.get_stock_info(country = "USA", ticker = usa_ticker)
            self.stock_repository.upsert_usa_stock(usa_stock)
            

            

        
        
    
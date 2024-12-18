import asyncio
from logs.logger import Logger
from kis_api.stock_kis_client import StockKisClient
from models.ticker import Ticker
from models.kor_stock import KORStock
from models.usa_stock import USAStock
from repositories.ticker_repository import TickerRepository
from repositories.stock_repository import StockRepository
from typing import List, Dict


class StockQuoteService:

    def __init__(self) -> None:
        self.logger = Logger(self.__class__.__name__)
        self.stock_kis_client = StockKisClient()
        self.ticker_repository = TickerRepository()
        self.stock_respository = StockRepository()
        
    def update_kor_stock_quotes(self) -> None:        
        kor_tickers: List[Ticker] = self.ticker_repository.fetch_kor_tickers()
        quote_data: List[Dict] = asyncio.run(self.stock_kis_client.fetch_kor_stock_quotes(kor_tickers))
        kor_quotes: List[KORStock] = self.process_kor_data(quote_data=quote_data)
        self.stock_respository.update_stock_quotes(country = "KOR", stock_quotes = kor_quotes)    
        self.logger.log_info(f"Updated {len(kor_quotes)} KOR stock quotes")
        
    def update_usa_stock_quotes(self) -> None:
        usa_tickers: List[Ticker] = self.ticker_repository.fetch_usa_tickers()    
        quote_data: List[Dict] = asyncio.run(self.stock_kis_client.fetch_usa_stock_quotes(usa_tickers))    
        usa_quotes: List[USAStock] = self.process_usa_data(quote_data=quote_data)
        self.stock_respository.update_stock_quotes(country = "USA", stock_quotes = usa_quotes)
        self.logger.log_info(f"Updated {len(usa_quotes)} USA stock quotes")
        
    def process_kor_data(self, quote_data: List[Dict]) -> List[KORStock]:
        kor_stocks = []
        for data in quote_data:
            try:
                kor_stock = KORStock.from_dict(
                    {
                        "ticker_id" : data["identifier"],
                        "open" : data["output"]["stck_oprc"],
                        "day_high" : data["output"]["stck_hgpr"],
                        "day_low" : data["output"]["stck_lwpr"],
                        "volume" : data["output"]["acml_vol"],
                        "close" : data["output"]["stck_prdy_clpr"],
                        "current_price" : data["output"]["stck_prpr"],
                    }
                )
                kor_stocks.append(kor_stock)
        
            except (KeyError, TypeError) as e:
                self.logger.log_error("Error fetching KOR stock quote...")
                self.logger.log_error(e)
                self.logger.log_error(data)
        return kor_stocks
        
    def process_usa_data(self, quote_data: List[Dict]) -> List[USAStock]:
        usa_stocks = []
        for data in quote_data:
            try:
                usa_stock = USAStock.from_dict(
                    {
                        "ticker_id" : data["identifier"],
                        "open" : data["output"]["open"],
                        "day_high" : data["output"]["high"],
                        "day_low" : data["output"]["low"],
                        "volume" : data["output"]["tvol"],
                        "close" : data["output"]["base"],
                        "current_price" : data["output"]["last"],
                    }
                )
                usa_stocks.append(usa_stock)
            except (KeyError, TypeError) as e:
                self.logger.log_error("Error fetching USA stock quote...")
                self.logger.log_error(e)
                self.logger.log_error(data)
        return usa_stocks
            
    
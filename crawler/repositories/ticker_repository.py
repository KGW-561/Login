from mysql.connector import Error
from typing import List, Dict
from repositories.base_repository import BaseRepository
from models.ticker import Ticker


class TickerRepository(BaseRepository):

    # 주식 티커 정보를 dict안에 넣는다
    # company(key) => ticker_id(value)
    def fetch_ticker_dict(self) -> Dict[str, str]:
        query = """
        SELECT 
            company, ticker_id 
        FROM 
            tickers
        """

        try:
            rows = self.fetch_results(query=query)
            return {row["company"]: row["ticker_id"] for row in rows}
        except Error as sql_e:
            self.logger.log_error("Error fetching ticker_dict")
            self.logger.log_error(sql_e)

    def fetch_tickers(self) -> List[Ticker]:
        query = """
        SELECT
            ticker_id,
            symbol
        FROM 
            tickers
        """
        
        try:
            rows = self.fetch_results(query = query)
            return [Ticker.from_dict(row) for row in rows]    
        except Error as sql_e:
            self.logger.log_error("Error fetching ALL Tickers")
            self.logger.log_error(sql_e)
        
    def fetch_kor_tickers(self) -> List[Ticker]:
        query = """
        SELECT
            ticker_id,
            exchange,
            symbol
        FROM 
            tickers
        WHERE
            country = 'KOR'
        """
        
        try:
            rows = self.fetch_results(query = query)
            return [Ticker.from_dict(row) for row in rows]
        except Error as sql_e:
            self.logger.log_error("Error fetching KOR Tickers")
            self.logger.log_error(sql_e)
            
    def fetch_usa_tickers(self) -> List[Ticker]:
        query = """
        SELECT
            ticker_id,
            exchange,
            symbol
        FROM 
            tickers
        WHERE
            country = 'USA'
        """
        
        try:
            rows = self.fetch_results(query = query)
            return [Ticker.from_dict(row) for row in rows]
        except Error as sql_e:
            self.logger.log_error("Error fetching USA Tickers")
            self.logger.log_error(sql_e)
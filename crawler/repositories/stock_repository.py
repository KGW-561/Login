from mysql.connector import Error
from repositories.base_repository import BaseRepository
from models.kor_stock import KORStock
from models.usa_stock import USAStock
from typing import List

class StockRepository(BaseRepository):
    
    def update_stock_quotes(self, country: str, stock_quotes: List[KORStock] | List[USAStock]) -> None:
        country_to_table = {
            "KOR" : "kor_stocks",
            "USA" : "usa_stocks"    
        }
        
        if country not in country_to_table:
            self.logger.log_error(f"Invalid country: {country}")
            return
        
        table = country_to_table.get(country)
        
        query = f"""
        UPDATE 
            {table}
        SET
            open = %s,
            day_high = %s,
            day_low = %s,
            volume = %s,
            close = %s,
            current_price = %s
        WHERE
            ticker_id = %s
        """
        
        values = [
            (
                stock_quote.open,
                stock_quote.day_high,
                stock_quote.day_low,
                stock_quote.volume,
                stock_quote.close,
                stock_quote.current_price,
                stock_quote.ticker_id
            )
            for stock_quote in stock_quotes
        ]
        
        try:
            self.execute_query(query = query, values = values, batch = True)
        except Error as sql_e:
            self.logger.log_error(f"Error updating {country} stocks.")            
            self.logger.log_error(sql_e)
            
    def upsert_kor_stock(self, kor_stock: KORStock) -> None:
        query = """
        INSERT INTO
            kor_stocks(
                ticker_id, 
                current_price, 
                close, 
                open, 
                volume, 
                fiftytwo_week_low, 
                fiftytwo_week_high, 
                day_low, 
                day_high, 
                return_on_assets, 
                return_on_equity, 
                enterprise_value, 
                enterprise_to_EBITDA, 
                price_to_book, 
                price_to_sales, 
                earnings_per_share, 
                current_ratio, 
                debt_to_equity
            )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY 
        UPDATE
            fiftytwo_week_low = VALUES(fiftytwo_week_low), 
            fiftytwo_week_high = VALUES(fiftytwo_week_high), 
            return_on_assets = VALUES(return_on_assets), 
            return_on_equity = VALUES(return_on_equity), 
            enterprise_value = VALUES(enterprise_value), 
            enterprise_to_EBITDA = VALUES(enterprise_to_EBITDA), 
            price_to_book = VALUES(price_to_book), 
            price_to_sales = VALUES(price_to_sales), 
            earnings_per_share = VALUES(earnings_per_share), 
            current_ratio = VALUES(current_ratio), 
            debt_to_equity = VALUES(debt_to_equity)
        """
        
        values = (
            kor_stock.ticker_id, 
            kor_stock.current_price, 
            kor_stock.close, 
            kor_stock.open, 
            kor_stock.volume, 
            kor_stock.fiftytwo_week_low, 
            kor_stock.fiftytwo_week_high, 
            kor_stock.day_low, 
            kor_stock.day_high, 
            kor_stock.return_on_assets, 
            kor_stock.return_on_equity, 
            kor_stock.enterprise_value, 
            kor_stock.enterprise_to_EBITDA, 
            kor_stock.price_to_book, 
            kor_stock.price_to_sales, 
            kor_stock.earnings_per_share, 
            kor_stock.current_ratio, 
            kor_stock.debt_to_equity
        )
            
        try:
            self.execute_query(query = query, values = values, batch = False)
        except Error as sql_e:
            self.logger.log_error("Error single inserting KOR stocks.")
            self.logger.log_error(sql_e)
                    
    def upsert_usa_stock(self, usa_stock: USAStock) -> None:
        query = """
        INSERT INTO
            usa_stocks(
                ticker_id, 
                current_price, 
                close, 
                open, 
                volume, 
                fiftytwo_week_low, 
                fiftytwo_week_high, 
                day_low, 
                day_high, 
                return_on_assets, 
                return_on_equity, 
                enterprise_value, 
                enterprise_to_EBITDA, 
                price_to_book, 
                price_to_sales, 
                earnings_per_share, 
                current_ratio, 
                debt_to_equity
            )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY 
        UPDATE
            fiftytwo_week_low = VALUES(fiftytwo_week_low), 
            fiftytwo_week_high = VALUES(fiftytwo_week_high), 
            return_on_assets = VALUES(return_on_assets), 
            return_on_equity = VALUES(return_on_equity), 
            enterprise_value = VALUES(enterprise_value), 
            enterprise_to_EBITDA = VALUES(enterprise_to_EBITDA), 
            price_to_book = VALUES(price_to_book), 
            price_to_sales = VALUES(price_to_sales), 
            earnings_per_share = VALUES(earnings_per_share), 
            current_ratio = VALUES(current_ratio), 
            debt_to_equity = VALUES(debt_to_equity)
        """
        
        values = (
            usa_stock.ticker_id, 
            usa_stock.current_price, 
            usa_stock.close, 
            usa_stock.open, 
            usa_stock.volume, 
            usa_stock.fiftytwo_week_low, 
            usa_stock.fiftytwo_week_high, 
            usa_stock.day_low, 
            usa_stock.day_high, 
            usa_stock.return_on_assets, 
            usa_stock.return_on_equity, 
            usa_stock.enterprise_value, 
            usa_stock.enterprise_to_EBITDA, 
            usa_stock.price_to_book, 
            usa_stock.price_to_sales, 
            usa_stock.earnings_per_share, 
            usa_stock.current_ratio, 
            usa_stock.debt_to_equity
        )
            
        try:
            self.execute_query(query = query, values = values, batch = False)
        except Error as sql_e:
            self.logger.log_error("Error inserting USA stocks.")
            self.logger.log_error(sql_e)
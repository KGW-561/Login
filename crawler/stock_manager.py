from services.stock_service import StockService
from services.stock_quote_service import StockQuoteService
from services.index_service import IndexService
from services.forex_service import ForexService
from logs.logger import Logger

class StockManager:
    
    def upsert_stock_info(self):
        stock_service = StockService()    
        stock_service.get_kor_stock_info()
        stock_service.get_usa_stock_info()
    
    def update_stock_quotes(self):
        stock_quote_service = StockQuoteService()
        stock_quote_service.update_kor_stock_quotes()
        stock_quote_service.update_usa_stock_quotes()
        
    def upsert_indices(self):
        index_service = IndexService()    
        index_service.upsert_indices()
        
    def upsert_forex(self):
        forex_service = ForexService()
        forex_service.upsert_forex()
    
    
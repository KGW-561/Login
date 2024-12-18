import yfinance as yf
from time import sleep
import random
from models.kor_stock import KORStock
from models.usa_stock import USAStock
from models.ticker import Ticker

# 주식 심볼을 사용하여 Ticker 객체 생성
# Ticker ID 예: Apple Inc의 주식 심볼 AAPL
#               삼성전자의 주식 심볼 005930.KS

class YFinanceClient:
        
    # 소수점 2자리로 반올림한다
    def format_decimals(self, value: float) -> float | None:
        if value is None:
            return value
        
        return round(value, 2)
    
    def convert_kor_ticker_format(self, kor_ticker_symbol) -> str:
        return kor_ticker_symbol + ".KS"
    
    def get_stock_info(self, country: str, ticker: Ticker) -> KORStock | USAStock | None:
        if country == "KOR":
            ticker.symbol = self.convert_kor_ticker_format(ticker.symbol)
            
        sleep(random.uniform(1,3))  

        if ticker.symbol == "BRK/A":
            ticker.symbol = "BRK.A"
        if ticker.symbol == "BF/B":
            ticker.symbol = "BF.B"
            
        try:
            yf_ticker = yf.Ticker(ticker.symbol)  
            info = yf_ticker.info
        except Exception as e:
            print(f"Ticker: {ticker}")
            print(e)
  
        if country == "KOR":
            
            kor_stock = KORStock.from_dict(    
                {
                    "ticker_id" : ticker.ticker_id,
                    "current_price" : self.format_decimals(info.get('currentPrice')),
                    "close" : self.format_decimals(info.get('previousClose')),
                    "open" : self.format_decimals(info.get('open')),
                    "volume" : info.get('volume'),
                    "fiftytwo_week_low": self.format_decimals(info.get('fiftyTwoWeekLow')),
                    "fiftytwo_week_high": self.format_decimals(info.get('fiftyTwoWeekHigh')),
                    "day_low": self.format_decimals(info.get('dayLow')),
                    "day_high": self.format_decimals(info.get('dayHigh')),
                    "return_on_assets": self.format_decimals(info.get('returnOnAssets')),
                    "return_on_equity": self.format_decimals(info.get('returnOnEquity')),
                    "enterprise_value": info.get('enterpriseValue'),
                    "enterprise_to_EBITDA": self.format_decimals(info.get('enterpriseToEbitda')),
                    "price_to_book": self.format_decimals(info.get('priceToBook')),
                    "price_to_sales": self.format_decimals(info.get('priceToSalesTrailing12Months')),
                    "earnings_per_share": self.format_decimals(info.get('trailingEps')),
                    "current_ratio": self.format_decimals(info.get('currentRatio')),
                    "debt_to_equity": self.format_decimals(info.get('debtToEquity'))
                }
            ) 
            
            print(kor_stock)
            
            return kor_stock
        
        usa_stock = USAStock.from_dict(    
                {
                    "ticker_id" : ticker.ticker_id,
                    "current_price" : self.format_decimals(info.get('currentPrice')),
                    "close" : self.format_decimals(info.get('previousClose')),
                    "open" : self.format_decimals(info.get('open')),
                    "volume" : info.get('volume'),
                    "fiftytwo_week_low": self.format_decimals(info.get('fiftyTwoWeekLow')),
                    "fiftytwo_week_high": self.format_decimals(info.get('fiftyTwoWeekHigh')),
                    "day_low": self.format_decimals(info.get('dayLow')),
                    "day_high": self.format_decimals(info.get('dayHigh')),
                    "return_on_assets": self.format_decimals(info.get('returnOnAssets')),
                    "return_on_equity": self.format_decimals(info.get('returnOnEquity')),
                    "enterprise_value": info.get('enterpriseValue'),
                    "enterprise_to_EBITDA": self.format_decimals(info.get('enterpriseToEbitda')),
                    "price_to_book": self.format_decimals(info.get('priceToBook')),
                    "price_to_sales": self.format_decimals(info.get('priceToSalesTrailing12Months')),
                    "earnings_per_share": self.format_decimals(info.get('trailingEps')),
                    "current_ratio": self.format_decimals(info.get('currentRatio')),
                    "debt_to_equity": self.format_decimals(info.get('debtToEquity'))
                }
            )
        
        print(usa_stock)
        
        return usa_stock
        


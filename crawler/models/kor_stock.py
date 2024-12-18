from decimal import Decimal
from typing import Dict


class KORStock:
    
    def __init__(
        self,
        kor_stock_id: int,
        ticker_id: int,
        current_price: Decimal,
        close: Decimal,
        open: Decimal,
        volume: int,
        fiftytwo_week_low: Decimal,
        fiftytwo_week_high: Decimal,
        day_low: Decimal,
        day_high: Decimal,
        return_on_assets: Decimal,
        return_on_equity: Decimal,
        enterprise_value: int,
        enterprise_to_EBITDA: Decimal,
        price_to_book: Decimal,
        price_to_sales: Decimal,
        earnings_per_share: Decimal,
        current_ratio: Decimal,
        debt_to_equity: Decimal
    ) -> None:
        self.kor_stock_id = kor_stock_id
        self.ticker_id = ticker_id
        self.current_price = current_price
        self.close = close
        self.open = open
        self.volume = volume
        self.fiftytwo_week_low = fiftytwo_week_low
        self.fiftytwo_week_high = fiftytwo_week_high
        self.day_low = day_low
        self.day_high = day_high
        self.return_on_assets = return_on_assets
        self.return_on_equity = return_on_equity
        self.enterprise_value = enterprise_value
        self.enterprise_to_EBITDA = enterprise_to_EBITDA
        self.price_to_book = price_to_book
        self.price_to_sales = price_to_sales
        self.earnings_per_share = earnings_per_share
        self.current_ratio = current_ratio
        self.debt_to_equity = debt_to_equity
        
    def __repr__(self) -> str:
        return f"""
        KORStock(
            kor_stock_id = {self.kor_stock_id},
            ticker_id = {self.ticker_id},
            current_price = {self.current_price},
            close = {self.close},
            open = {self.open},
            volume = {self.volume},
            fiftytwo_week_low = {self.fiftytwo_week_low},
            fiftytwo_week_high = {self.fiftytwo_week_high},
            day_low = {self.day_low},
            day_high = {self.day_high},
            return_on_assets = {self.return_on_assets},
            return_on_equity = {self.return_on_equity},
            enterprise_value = {self.enterprise_value},
            enterprise_to_EBITDA = {self.enterprise_to_EBITDA},
            price_to_book = {self.price_to_book},
            price_to_sales = {self.price_to_sales},
            earnings_per_share = {self.earnings_per_share},
            current_ratio = {self.current_ratio},
            debt_to_equity = {self.debt_to_equity}
        )
        """
    
    def to_dict(self) -> Dict:
        return {    
            "kor_stock_id" : self.kor_stock_id,
            "ticker_id" : self.ticker_id,
            "current_price" : self.current_price,
            "close" : self.close,
            "open" : self.open,
            "volume" : self.volume,
            "fiftytwo_week_low" : self.fiftytwo_week_low,
            "fiftytwo_week_high" : self.fiftytwo_week_high,
            "day_low" : self.day_low,
            "day_high" : self.day_high,
            "return_on_assets" : self.return_on_assets,
            "return_on_equity" : self.return_on_equity,
            "enterprise_value" : self.enterprise_value,
            "enterprise_to_EBITDA" : self.enterprise_to_EBITDA,
            "price_to_book" : self.price_to_book,
            "price_to_sales" : self.price_to_sales,
            "earnings_per_share" : self.earnings_per_share,
            "current_ratio" : self.current_ratio,
            "debt_to_equity" : self.debt_to_equity
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "KORStock":
        return cls(
            kor_stock_id = data.get("kor_stock_id"),
            ticker_id = data.get("ticker_id"),
            current_price = data.get("current_price"),
            close = data.get("close"),
            open = data.get("open"),
            volume = data.get("volume"),
            fiftytwo_week_low = data.get("fiftytwo_week_low"),
            fiftytwo_week_high = data.get("fiftytwo_week_high"),
            day_low = data.get("day_low"),
            day_high = data.get("day_high"),
            return_on_assets = data.get("return_on_assets"),
            return_on_equity = data.get("return_on_equity"),
            enterprise_value = data.get("enterprise_value"),
            enterprise_to_EBITDA = data.get("enterprise_to_EBITDA"),
            price_to_book = data.get("price_to_book"),
            price_to_sales = data.get("price_to_sales"),
            earnings_per_share = data.get("earnings_per_share"),
            current_ratio = data.get("current_ratio"),
            debt_to_equity = data.get("debt_to_equity"),
        )
    
        
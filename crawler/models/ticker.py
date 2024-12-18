from typing import Dict


class Ticker:
    
    def __init__(
        self, 
        ticker_id: int, 
        exchange: str,
        symbol: str,
        company: str
    ) -> None:
        self.ticker_id = ticker_id
        self.exchange = exchange
        self.symbol = symbol
        self.company = company
        
    def __repr__(self) -> str:
        return f"""
        Ticker(
            ticker_id = {self.ticker_id},
            exchange = {self.exchange},
            symbol = {self.symbol},
            company = {self.company}
        )
        """
        
    def to_dict(self) -> Dict:
        return {
            "ticker_id" : self.ticker_id,
            "exchange" : self.exchange,
            "symbol" : self.symbol,
            "company" : self.company,
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "Ticker":
        return cls(
            ticker_id = data.get("ticker_id"),
            exchange = data.get("exchange"),
            symbol = data.get("symbol"),
            company = data.get("company"),
        )
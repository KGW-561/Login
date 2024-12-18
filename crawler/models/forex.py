from decimal import Decimal
from datetime import datetime
from typing import Optional, Dict


class Forex:
    
    def __init__(self, 
                 forex_id: int, 
                 forex_name: str, 
                 rate: Decimal, 
                 change_value: Decimal,
                 change_percent: Decimal,
                 last_updated: datetime
                ) -> None:
    
        self.forex_id = forex_id
        self.forex_name = forex_name
        self.rate = rate
        self.change_value = change_value
        self.change_percent = change_percent
        self.last_updated = last_updated
    
    def __repr__(self) -> str:
        return f"""
    Forex(
        forex_id = {self.forex_id},
        forex_name = {self.forex_name},
        rate = {self.rate},
        change_value = {self.change_value},
        change_percent = {self.change_percent},
        last_updated = {self.last_updated}
    )
    """
    
    def to_dict(self) -> Dict:
        return {
            "forex_id" : self.forex_id,
            "forex_name" : self.forex_name,
            "rate" : self.rate,
            "change_value" : self.change_value,
            "change_percent" : self.change_percent,
            "last_updated" : self.last_updated
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "Forex":
        return cls(
            forex_id = data.get("forex_id"),
            forex_name = data.get("forex_name"),
            rate = data.get("rate"),
            change_value = data.get("change_value"),
            change_percent = data.get("change_percent"),
            last_updated = data.get("last_updated")
        )
    
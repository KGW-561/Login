from decimal import Decimal
from typing import Dict


class Index:
    
    def __init__(
        self,
        index_id: int,
        title: str,
        current_value: Decimal,
        change_value: Decimal,
        change_percent: Decimal
    ) -> None:
        self.index_id = index_id
        self.title = title
        self.current_value = current_value
        self.change_value = change_value
        self.change_percent = change_percent
        
    def __repr__(self) -> str:
        return f"""
        Index(
            index_id = {self.index_id},
            title = {self.title},
            current_value = {self.current_value},
            change_value = {self.change_value},
            change_percent = {self.change_percent}
        )
        """
        
    def to_dict(self) -> Dict:
        return {
            "index_id" : self.index_id,
            "title" : self.title,
            "current_value" : self.current_value,
            "change_value" : self.change_value,
            "change_percent" : self.change_percent,
        }
        
    @classmethod
    def from_dict(cls, data: Dict) -> "Index":
        return cls(
            index_id = data.get("index_id"),
            title = data.get("title"),
            current_value = data.get("current_value"),
            change_value = data.get("change_value"),
            change_percent = data.get("change_percent")
        )
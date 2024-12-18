import asyncio
from typing import List, Dict
from logs.logger import Logger
from models.forex import Forex
from kis_api.forex_kis_client import ForexKisClient
from repositories.forex_repository import ForexRepository


class ForexService:
    
    def __init__(self) -> None:
        self.logger = Logger(self.__class__.__name__)
        self.forex_kis_client = ForexKisClient()
        self.forex_repository = ForexRepository()
        
    def upsert_forex(self) -> None:
        forex_infos = [
            {
                "title" : "KRW/USD",
                "iscd" : "FX@KRW"
            }
        ]
        
        forexes_data: List[Dict] = asyncio.run(self.forex_kis_client.fetch_forex(forex_infos))
        forexes: List[Forex] = self.process_data(forexes_data)
        self.forex_repository.upsert_forex(forexes)
        self.logger.log_info(f"Updated {len(forexes)} forex.")
        
    def process_data(self, forexes_data: List[Dict]) -> List[Forex]:
        forexes = []
        for data in forexes_data:
            try:
                forex = Forex.from_dict(
                    {
                        "forex_name" : data["identifier"],
                        "rate" : data["output1"]["ovrs_nmix_prpr"],
                        "change_value" : data["output1"]["ovrs_nmix_prdy_vrss"],
                        "change_percent" : data["output1"]["prdy_ctrt"]
                    }        
                ) 
                forexes.append(forex)
            except (KeyError, TypeError) as e:
                self.logger.log_error("Error fetching forex...")
                self.logger.log_error(e)
                self.logger.log_error(data)
                
        return forexes
        
        
        
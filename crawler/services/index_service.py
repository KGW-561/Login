from logs.logger import Logger
from typing import List, Dict
import asyncio
from models.index import Index
from kis_api.index_kis_client import IndexKisClient
from repositories.index_repository import IndexRepository

class IndexService:
    
    def __init__(self) -> None:
        self.logger = Logger(self.__class__.__name__)
        self.index_kis_client = IndexKisClient()
        self.index_repository = IndexRepository()
    
    def upsert_indices(self) -> None:
        kor_index_infos = [
            {
                "title" : "KOSPI",
                "fid" : "0001"
            },
            {
                "title" : "KOSDAQ",
                "fid" : "1001"
            }
        ]
        
        usa_index_infos = [
            {
                "title" : "NASDAQ",
                "iscd" : "COMP"
            },
            {
                "title" : "S&P500",
                "iscd" : "SPX"
            }
        ]
        
        indices = []
        
        kor_indices_data = asyncio.run(self.index_kis_client.fetch_kor_index(kor_index_infos))
        self.logger.log_info(f"Fetched {len(kor_indices_data)} KOR indices data.")
        usa_indices_data = asyncio.run(self.index_kis_client.fetch_usa_index(usa_index_infos))
        self.logger.log_info(f"Fetched {len(usa_indices_data)} USA indices data.")
        
        kor_indices: List[Index] = self.process_kor_data(kor_indices_data)
        usa_indices: List[Index] = self.process_usa_data(usa_indices_data)
        
        indices.extend(kor_indices)
        indices.extend(usa_indices)
        
        self.index_repository.upsert_index(indices)
        self.logger.log_info(f"Updated {len(indices)} indices.")
        
    def process_kor_data(self, indices_data: List[Dict]) -> List[Index]:
        kor_indices = []
        for data in indices_data:
            try:
                kor_index = Index.from_dict(
                    {
                        "title" : data["identifier"],
                        "current_value" : data["output"]["bstp_nmix_prpr"],
                        "change_value" : data["output"]["bstp_nmix_prdy_vrss"],
                        "change_percent" : data["output"]["bstp_nmix_prdy_ctrt"]
                    }            
                )
                kor_indices.append(kor_index)
            except (KeyError, TypeError) as e:
                self.logger.log_error("Error fetching KOR index data...")
                self.logger.log_error(e)
                self.logger.log_error(data)
                
        return kor_indices

    def process_usa_data(self, indices_data: List[Dict]) -> List[Index]:
        usa_indices = []
        for data in indices_data:
            try:
                usa_index = Index.from_dict(
                     {
                        "title" : data["identifier"],
                        "current_value" : data["output1"]["ovrs_nmix_prpr"],
                        "change_value" : data["output1"]["ovrs_nmix_prdy_vrss"],
                        "change_percent" : data["output1"]["prdy_ctrt"]
                    }     
                )
                usa_indices.append(usa_index)
            except (KeyError, TypeError) as e:
                self.logger.log_error("Error fetching USA index data...")
                self.logger.log_error(e)
                self.logger.log_error(data)
                
        return usa_indices
    
    
    

        
        
        
        
from mysql.connector import Error
from repositories.base_repository import BaseRepository
from typing import List
from models.forex import Forex


class ForexRepository(BaseRepository):
    
    def upsert_forex(self, forexes: List[Forex]) -> None:
        query = """
        INSERT INTO forex (forex_name, rate, change_value, change_percent, last_updated) 
        VALUES (%s, %s, %s, %s, NOW())
        ON DUPLICATE KEY 
        UPDATE
            rate = VALUES(rate),
            change_value = VALUES(change_value),
            change_percent = VALUES(change_percent),
            last_updated = VALUES(last_updated)
        """
        
        # api로 크롤링한 환율 정보
        values = [    
            (
                forex.forex_name,
                forex.rate,
                forex.change_value,
                forex.change_percent,
            )   
            for forex in forexes
        ]
        
        try:
            self.execute_query(query = query, values = values, batch = True)
        except Error as sql_e:
            self.logger.log_error("Error upserting forex.")
            self.logger.log_error(sql_e)
            
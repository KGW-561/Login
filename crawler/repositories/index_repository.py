from mysql.connector import Error
from repositories.base_repository import BaseRepository
from models.index import Index
from typing import List

class IndexRepository(BaseRepository):
    
    def upsert_index(self, indices: List[Index]) -> None:
        query = '''
        INSERT INTO indices (title, current_value, change_value, change_percent) 
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY 
        UPDATE
            current_value = VALUES(current_value),
            change_value = VALUES(change_value),
            change_percent = VALUES(change_percent);
        '''
        
        values = [    
            (
                index.title,
                index.current_value,
                index.change_value,
                index.change_percent,
            )
            for index in indices
        ]
        
        try:
            self.execute_query(query = query, values = values, batch = True)
        except Error as sql_e:
            self.logger.log_error("Error upserting index.")
            self.logger.log_error(sql_e)
            
            
from mysql.connector import Error
from repositories.base_repository import BaseRepository
from enums.log_msg import LogMsg
from typing import List, Dict
from datetime import datetime

class CrawlerRepository(BaseRepository):

    def save_crawled_articles(self, item: Dict) -> None:
        # 데이터베이스 연결이 안된 경우
        if not self.connection and not self.connection.is_connected(): 
            raise Error("Error connecting to Database. Check if connection is initialized")

        # 데이터베이스에 입력할 기사가 없을 경우
        if not item.get("content"): 
            self.logger.log_error("There is no article content to insert.")
            return

        # INSERT IGNORE로 중복 데이터는 받지 않는다
        # link 칼럼에 이미 UNIQUE 제약 조건을 걸었다.
        query = """
        INSERT IGNORE INTO 
            raw_news(country, title, image_link, source, content, published_at, link) 
        VALUES 
            (%s, %s, %s, %s, %s, %s, %s)
        """
        
        # Scrapy에서 크롤링한 기사 정보
        values = (
            item["country"],
            item["title"],
            item["image_link"],
            item["source"],
            item["content"],
            item["published_at"],
            item["link"],
        )

        try:
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            self.connection.commit()
            
            # 마지막에 삽입한 
            if cursor.rowcount > 0:
                self.last_row_id = cursor.lastrowid 
            else:
                self.last_row_id = None
        except Error as sql_e:
            self.logger.log_error("Error inserting crawled article.")
            self.logger.log_error(sql_e)
        finally:
            cursor.close()

    def create_log(self) -> None:
        # 데이터베이스에 연결이 안된 경우
        if not self.connection and not self.connection.is_connected():
            raise Error("Error connecting to Database. Check if connection is initialized.")
        
        if not self.last_row_id:
            self.logger.log_info("No log has been created")
            return

        query = """
        INSERT INTO 
            news_process_logs(raw_news_id, crawled_at, log_msg) 
        VALUES 
            (%s, NOW(), %s)
        """

        # 뉴스 기사 원본을 삽입하고 받은 PK값을 넣는다 (self.last_row_id)
        values = (self.last_row_id, LogMsg.CRAWLED_SUCCESS.value)

        try:
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            self.connection.commit()
        except Error as sql_e:
            self.logger.log_error(f"Error creating News Process Log. raw_news_id #{self.last_row_id}")
            self.logger.log_error(sql_e)
        finally:
            cursor.close()
            
    def get_latest_published_dates_by_website(self) -> List[Dict[str, datetime]]:
        query = """
        SELECT 
            source,
            MAX(published_at) AS latest_published_at
        FROM 
            raw_news
        GROUP BY 
            source
        """
        
        try:
            rows = self.fetch_results(query=query)
            return [{row.get('source') : row.get('latest_published_at')} for row in rows]
        except Error as sql_e:
            self.logger.log_error(f"Error fetching latest timestamp")
            self.logger.log_error(sql_e)
        

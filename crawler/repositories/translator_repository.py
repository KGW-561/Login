from mysql.connector import Error
from typing import List
from repositories.base_repository import BaseRepository
from models.article import Article


class TranslatorRepository(BaseRepository):

    # 번역이 안된 영문 기사들을 데이터베이스에서 가져온다
    def fetch_unprocessed_data(self) -> List[Article]:
        # 실제 테이블용 쿼리
        query = """
        SELECT
            rn.raw_news_id,
            rn.title,
            rn.content
        FROM 
            raw_news rn
        JOIN
            news_process_logs npl ON npl.raw_news_id = rn.raw_news_id
        WHERE
            npl.translated_at IS NULL
            AND npl.completed_at IS NULL
            AND npl.process_status = 'SUCCESS'
            AND rn.country = 'USA'
        """

        try:
            rows = self.fetch_results(query=query)
            return [
                Article.from_dict(row) for row in rows
            ]  # 가져온 기사 정보를 Article 객체에 담음
        except Error as sql_e:
            self.logger.log_error("Error fetching untranslated articles.")
            self.logger.log_error(sql_e)
            return []

    # 번역된 영문 기사들을 데이터베이스에 저장
    def save_processed_data(self, articles: List[Article]) -> None:

        query = """
        INSERT INTO
            translated_news(raw_news_id, title, content)
        VALUES
            (%s, %s, %s)
        """

        values = [
            (article.raw_news_id, article.title, article.content)
            for article in articles
        ]

        try:
            self.execute_query(query=query, values=values, batch=True)
        except Error as sql_e:
            self.logger.log_error("Error inserting translated articles.")
            self.logger.log_error(sql_e)

from mysql.connector import Error
from typing import List
from repositories.base_repository import BaseRepository
from models.article import Article


class SentimentAnalyzerRepository(BaseRepository):

    # 감정 평가가 안된 기사를 데이터베이스에서 가져온다
    def fetch_unprocessed_data(self) -> List[Article] | None:

        # 주식 뉴스라고 분류된 기사들만 가져온다
        query = """
        SELECT
            DISTINCT ken.raw_news_id,
            CASE
                WHEN rn.country = 'KOR' THEN rn.content
                ELSE tn.content
            END AS content
        FROM
            keyword_extracted_news ken
        JOIN
            raw_news rn ON rn.raw_news_id = ken.raw_news_id
        JOIN
            translated_news tn ON tn.raw_news_id = ken.raw_news_id
        JOIN
            news_process_logs npl ON npl.raw_news_id = ken.raw_news_id
        WHERE
            ken.news_type = 'stock'
            AND npl.sentiment_analyzed_at IS NULL
            AND npl.process_status = 'SUCCESS'
            AND npl.completed_at IS NULL;
        """

        try:
            rows = self.fetch_results(query=query)
            return [
                Article.from_dict(row) for row in rows
            ]  # Article 객체 배열에 결과 저장
        except Error as sql_e:
            self.logger.log_error("Error fetching unanalyzed(sentiment) articles.")
            self.logger.log_error(sql_e)
            return None

    # 감정 평가가 된 뉴스 기사들을 데이터베이스에 저장한다
    def save_processed_data(self, articles: List[Article]) -> None:

        query = """
        INSERT INTO 
            sentiment_analyzed_news(raw_news_id, sentiment)
        VALUES
            (%s, %s)
        """

        values = [(article.raw_news_id, article.sentiment) for article in articles]

        try:
            self.execute_query(query=query, values=values, batch=True)
        except Error as sql_e:
            self.logger.log_error("Error inserting sentiment analyzed articles.")
            self.logger.log_error(sql_e)

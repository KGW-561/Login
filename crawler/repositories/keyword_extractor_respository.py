from mysql.connector import Error
from repositories.base_repository import BaseRepository
from models.article import Article
from typing import List


class KeywordExtractorRepository(BaseRepository):

    # 키워드 추출이 안된 기사들을 데이터베이스에서 가져온다
    def fetch_unprocessed_data(self) -> List[Article] | None:

        # 원본이 영문이라면 번역된 기사를 가져온다
        query = """
        SELECT
            rn.raw_news_id,
            CASE
                WHEN rn.country = 'KOR' THEN rn.title
                ELSE tn.title
            END AS title,
            CASE
                WHEN rn.country = 'KOR' THEN rn.content
                ELSE tn.content
            END AS content
        FROM
            raw_news rn
        JOIN
            news_process_logs npl ON npl.raw_news_id = rn.raw_news_id
        LEFT JOIN
            translated_news tn ON tn.raw_news_id = rn.raw_news_id
        WHERE
            npl.keyword_extracted_at IS NULL
            AND npl.process_status = 'SUCCESS'
            AND npl.completed_at IS NULL
        """

        try:
            rows = self.fetch_results(query=query)
            return [Article.from_dict(row) for row in rows]  # Article 배열에 결과 저장
        except Error as sql_e:
            self.logger.log_error("Error fetching unextracted(keyword) articles.")
            self.logger.log_error(sql_e)
            return None

    # 키워드 추출된 기사의 정보를 저장: 해당 기사의 뉴스 분류(경제/주식), 티커 id
    def save_processed_data(self, articles: List[Article]) -> None:

        query = """
        INSERT INTO
            keyword_extracted_news(raw_news_id, news_type, ticker_id)
        VALUES
            (%s, %s, %s)
        """

        values = [
            (article.raw_news_id, article.news_type, article.ticker_id)
            for article in articles
        ]

        try:
            self.execute_query(query=query, values=values, batch=True)
        except Error as sql_e:
            self.logger.log_error("Error inserting sentiment analyzed articles.")
            self.logger.log_error(sql_e)

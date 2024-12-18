from repositories.base_repository import BaseRepository
from models.article import Article
from mysql.connector import Error
from typing import List


class ExportRepository(BaseRepository):

    # 텍스트 가공 단계를 다 거친 뉴스 기사들을 데이터베이스에서 가져온다
    def fetch_processed_data(self) -> List[Article]:

        # 번역된 뉴스 기사라면 translated_news 테이블에서 번역된 기사 제목과 내용을 가져온다
        query = """
        SELECT
            rn.raw_news_id,
            rn.country,
            CASE
                WHEN rn.country = 'KOR' THEN rn.title
                ELSE tn.title
            END AS title,
            rn.image_link,
            rn.source,
            CASE
                WHEN rn.country = 'KOR' THEN rn.content
                ELSE tn.content
            END AS content,
            rn.published_at,
            rn.link,
            ken.news_type,
            ken.ticker_id,
            san.sentiment,
            tn.title as translated_title,
            tn.content as translated_content
        FROM
            raw_news rn
        JOIN
            keyword_extracted_news ken ON ken.raw_news_id = rn.raw_news_id
        JOIN
            news_process_logs npl ON npl.raw_news_id = rn.raw_news_id
        LEFT JOIN
            sentiment_analyzed_news san ON san.raw_news_id = rn.raw_news_id            
        LEFT JOIN
            translated_news tn ON tn.raw_news_id = rn.raw_news_id
        WHERE
            npl.completed_at IS NULL
            AND npl.process_status = 'SUCCESS';
        """

        try:
            rows = self.fetch_results(query=query)
        except Error as sql_e:
            self.logger.log_error("Error fetching completed articles")
            self.logger.log_error(sql_e)
        return [Article.from_dict(row) for row in rows]

    # 경제 뉴스를 데이터베이스에 입력
    def insert_econ_news(self, country: str, econ_articles: List[Article]) -> None:
        # 나라와 테이블 매핑
        country_to_table = {"KOR": "kor_econ_news", "USA": "usa_econ_news"}

        table = country_to_table.get(country)  # 해당 나라에 맞는 테이블명
        if not table:  # 매핑이 안된 country일 경우 조기 반환
            self.logger.log_error(f"Not a valid country: {country}")
            return

        query = f"""
        INSERT INTO
            {table}(title, source, image_link, content, published_at, link)
        VALUES
            (%s, %s, %s, %s, %s, %s)
        """

        values = [
            (
                article.title,
                article.source,
                article.image_link,
                article.content,
                article.published_at,
                article.link,
            )
            for article in econ_articles
        ]

        try:
            self.execute_query(query=query, values=values, batch=True)
        except Error as sql_e:
            self.logger.log_error("Error inserting econ news(KOR/USA).")
            self.logger.log_error(values)
            self.logger.log_error(sql_e)

    # 주식 뉴스를 데이터베이스에 입력
    def insert_stock_news(self, country: str, stock_articles: list[Article]) -> None:

        # 나라와 테이블 매핑
        country_to_table = {"KOR": "kor_stock_news", "USA": "usa_stock_news"}

        table = country_to_table.get(country)  # 해당 나라에 맞는 테이블명
        if not table:  # 매핑이 안된 country일 경우 조기 반환
            self.logger.log_error(f"Not a valid country: {country}")
            return

        query = f"""
        INSERT INTO
            {table} (title, source, image_link, content, published_at, link, ticker_id, sentiment)
        VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = [
            (
                article.title,
                article.source,
                article.image_link,
                article.content,
                article.published_at,
                article.link,
                article.ticker_id,
                article.sentiment,
            )
            for article in stock_articles
        ]

        try:
            self.execute_query(query=query, values=values, batch=True)
        except Error as sql_e:
            self.logger.log_error("Error inserting stock news(KOR/USA)")
            self.logger.log_error(values)
            self.logger.log_error(sql_e)

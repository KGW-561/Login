from mysql.connector import Error
from typing import List

from models.news_process_log import NewsProcessLog
from repositories.base_repository import BaseRepository
from enums.process import Process


class NewsProcessLogRepository(BaseRepository):

    # 텍스트 가공 로그를 업데이트 한다
    def update_logs(self, process: Process, logs: List[NewsProcessLog]) -> None:
        if not logs:
            self.logger.log_warning("There are no logs to update.")
            return

        query = None
        values = None

        # 각 텍스트 가공 단계와 업데이트할 칼럼 매핑
        process_to_column = {
            Process.TRANSLATION: "translated_at",
            Process.KEYWORD_EXTRACTION: "keyword_extracted_at",
            Process.SENTIMENT_ANALYSIS: "sentiment_analyzed_at",
            Process.COMPLETED: "completed_at",
        }

        if process not in process_to_column:
            self.logger.log_error(f"Process value not in enum class Process: {process}")
            return

        column_name = process_to_column.get(process)

        # 텍스트 가공에 실패했을 경우 해당 기사에 대한 가공은 끝났다고 정의한다 (completed_at = NOW())
        # 성공했을 경우 completed_at은 null 상태로 남아있는다
        query = f'''
        UPDATE
            news_process_logs
        SET
            {column_name} = NOW(),
            completed_at = CASE
                WHEN %s = 'FAILED' THEN NOW()
                ELSE completed_at
            END,
            process_status = %s,
            log_msg = %s
        WHERE
            raw_news_id = %s
        '''

        values = [
            (log.status, log.status, log.log_msg, log.raw_news_id) for log in logs
        ]

        try:
            self.execute_query(query=query, values=values, batch=True)
        except Error as sql_e:
            self.logger.log_error("Error updating news process logs.")
            self.logger.log_error(sql_e)

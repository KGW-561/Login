import os
import json
from abc import ABC
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from typing import List

from logs.logger import Logger


class BaseRepository(ABC):

    BATCH_SIZE = 200 # batch 삽입/업데이트 제한 수

    # env 파일에서 환경변수를 가져온다
    def __init__(self) -> None:
        load_dotenv()
        self.database = os.getenv("MYSQL_DATABASE")
        self.host = os.getenv("MYSQL_HOST")
        self.port = os.getenv("MYSQL_PORT")
        self.user = os.getenv("MYSQL_USER")
        self.password = os.getenv("MYSQL_PASSWORD")
        self.logger = Logger(self.__class__.__name__)
        self.connection = None

    # 데이터베이스에 연결
    def connect(self) -> None:
        try:
            self.connection = mysql.connector.connect(
                database=self.database,
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
            )
            self.logger.log_info("Connected to MySQL Database.")
        except Error as sql_e:
            self.connection = None
            raise Error(f"Error connecting to MySQL Database. Reason: {sql_e}")

    # 데이터베이스에서 연결 해제
    def disconnect(self) -> None:
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.logger.log_info("Disconnected from MySQL Database.")
        else:
            raise Error("Error disconnecting from MySQL Database. Check if connection is made.")

    # DML문 실행을 위한 함수
    # batch: batch insert하는 기능
    def execute_query(self, query: str, values, batch: bool = False) -> None:
        # VALUES()에 들어가는 입력 값이 없다면 로그로 경고
        if not values:
            self.logger.log_warning("There are no records to insert.")

        try:
            # 데이터베이스 연결이 안되어있으면 미리 연결
            if self.connection == None or not self.connection.is_connected():
                self.connect()

            cursor = self.connection.cursor()
            # batch 삽입 시 전체 VALUES() 값을 나누어서 실행한다
            if batch:
                for idx in range(0, len(values), self.BATCH_SIZE):
                    chunk = values[idx : idx + self.BATCH_SIZE]
                    cursor.executemany(query, chunk)
                    self.connection.commit()

                    self.logger.log_info("Inserting/Updating records by batch.")
            else:
                # 단일 삽입
                cursor.execute(query, values)
                self.connection.commit()
                self.last_row_id = cursor.lastrowid

                self.logger.log_info("Inserting/Updating record.")
        except Error as sql_e:
            raise Error(f"Error executing query. Reason: {sql_e}")
        finally:
            cursor.close()
            if self.connection and self.connection.is_connected():
                self.disconnect()

    # DQL문 실행을 위한 함수
    # all: 결과 전체를 가져온다
    def fetch_results(self, query: str, all: bool = True) -> List:
        # 데이터베이스 연결이 안되어있으면 미리 연결
        if self.connection == None or not self.connection.is_connected():
            self.connect()
            
        # 데이터베이스에서 가져오는 값을 dictionary로 받는다
        cursor = self.connection.cursor(dictionary=True)
        try:
            # 여러 값을 받는 경우 fetchall()로 결과 값들을 가져온다
            if all:
                cursor.execute(query)
                rows = cursor.fetchall()
                if not rows:
                    self.logger.log_warning("No records have been fetched.")
                else:
                    self.logger.log_info("Fetching records.")
                return rows # 결과 값들 반환 -> List[Dict]

            else:
                # 결과 값 하나만 필요할 시
                row = cursor.execute(query)
                if not row:
                    self.logger.log_warning("No record has been fetched.")
                else:
                    self.logger.log_info("Fetching record.")
                    self.logger.log_info(row)
                return row # 결과 값 반환 -> Dict
        except Error as sql_e:
            raise Error(f"Error fetching results. Reason: {sql_e}")
        finally:
            cursor.close()
            self.disconnect()

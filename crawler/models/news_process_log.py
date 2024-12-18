from enums.status import Status
from enums.log_msg import LogMsg


class NewsProcessLog:

    def __init__(self, raw_news_id: int, status: str, log_msg: str):
        self.raw_news_id = raw_news_id
        self.status = status
        self.log_msg = log_msg

    # 객체를 print할 때
    # Java의 to_string() 메소드와 동일
    def __repr__(self) -> str:
        return f"""
    NewsProcessLog(
        raw_news_id = {self.raw_news_id},
        status = {self.status},
        log_msg = {self.log_msg}
    )
    """

    # dictionary로 객체 생성
    @classmethod
    def from_dict(cls, data: dict) -> "NewsProcessLog":
        return cls(
            raw_news_id=data.get("raw_news_id"),
            status=data.get("status"),
            log_msg=data.get("log_msg"),
        )

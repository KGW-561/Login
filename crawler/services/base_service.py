from abc import ABC, abstractmethod
from typing import List
from models.news_process_log import NewsProcessLog


class BaseService(ABC):

    @abstractmethod
    def process(self) -> List[NewsProcessLog]:
        pass

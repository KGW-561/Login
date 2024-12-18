from enum import Enum


class Process(Enum):
    TRANSLATION = "translation"
    KEYWORD_EXTRACTION = "keyword_extraction"
    SENTIMENT_ANALYSIS = "sentiment_analysis"
    COMPLETED = "completed"

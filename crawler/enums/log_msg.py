from enum import Enum


class LogMsg(Enum):
    CRAWLED_SUCCESS = "Successfully crawled article."

    TRANSLATION_SUCCESS = "Successfully translated article."
    TRANSLATION_FAILED = "Failed to translate article #{article_id}. \n Error: {reason}"

    KEYWORD_EXTRACTION_SUCCESS = "Successfully extracted keyword from article."
    # KEYWORD_EXTRACTION_FAILED = ''

    SENTIMENT_ANALYSIS_SUCCESS = "Successfully analyzed sentiment from article."
    SENTIMENT_ANALYSIS_FAILED = (
        "Failed to analyze sentiment from article #{article_id}. \nError: {reason}"
    )

    PROCESS_COMPLETED = "Successfully completed the entire process."

    def format_failed_msg(self, **kwargs) -> str:
        return self.value.format(**kwargs)

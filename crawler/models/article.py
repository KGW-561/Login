from typing import Optional, Dict


class Article:

    def __init__(
        self,
        raw_news_id: Optional[int] = None,
        country: Optional[str] = None,
        title: Optional[str] = None,
        image_link: Optional[str] = None,
        source: Optional[str] = None,
        content: Optional[str] = None,
        published_at: Optional[str] = None,
        link: Optional[str] = None,
        news_type: Optional[str] = None,
        ticker_id: Optional[str] = None,
        sentiment: Optional[str] = None,
    ) -> None:
        self.raw_news_id = raw_news_id
        self.country = country
        self.title = title
        self.image_link = image_link
        self.source = source
        self.content = content
        self.published_at = published_at
        self.link = link
        self.news_type = news_type
        self.ticker_id = ticker_id
        self.sentiment = sentiment

    # 객체를 출력할 때
    # Java의 to_string()과 동일
    def __repr__(self) -> str:
        return f"""
        Article(
            raw_news_id = {self.raw_news_id if self.raw_news_id else ''}, 
            country = {self.country if self.country else ''},
            title = {self.title if self.title else ''}, 
            image_link = {self.image_link if self.image_link else ''},
            source = {self.source if self.source else ''},
            content = {self.content[:50] if self.content else ''}..., 
            published_date = {self.published_at if self.published_at else ''},
            link = {self.link if self.link else ''}, 
            news_type = {self.news_type if self.news_type else ''},
            ticker_id = {self.ticker_id if self.ticker_id else ''},
            sentiment = {self.sentiment if self.sentiment else ''}
        )
        """

    def to_dict(self) -> Dict:
        return {
            "raw_news_id": self.raw_news_id,
            "country": self.country,
            "title": self.title,
            "image_link": self.image_link,
            "source": self.source,
            "content": self.content,
            "published_at": self.published_at,
            "link": self.link,
            "translated_content": self.translated_content,
            "news_type": self.news_type,
            "ticker_id": self.ticker_id,
            "sentiment": self.sentiment,
        }

    # dictionary로 객체 생성
    @classmethod
    def from_dict(cls, data: Dict) -> "Article":
        return cls(
            raw_news_id=data.get("raw_news_id"),
            country=data.get("country"),
            title=data.get("title"),
            image_link=data.get("image_link"),
            source=data.get("source"),
            content=data.get("content"),
            published_at=data.get("published_at"),
            link=data.get("link"),
            news_type=data.get("news_type"),
            ticker_id=data.get("ticker_id"),
            sentiment=data.get("sentiment"),
        )

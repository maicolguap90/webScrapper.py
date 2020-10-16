from sqlalchemy import Column, String, Interger

from base import Base

class Article(Base):
    __tablename__='article'

    id = Column(String, primary_key=True)
    body = Column(String)
    host = Column(String)
    title = Column(String)
    newspaper_uid = Column(String)
    n_tokens_body = Column(Interger)
    n_tokens_title = Column(Interger)
    url = Column(String, unique=True)

    def __init__(self,
                 uid,
                 body,
                 host,
                 newspaper_uid,
                 n_tokens_body,
                 n_tokens_title,
                 title,
                 url):
        self.id = uid
        self.body = body
        self.host = host
        self.newspaper_uid = newspaper_uid
        self.n_tokens_body = n_tokens_body
        self.n_tokens_title = n_tokens_title
        self.title = title
        self.url = url
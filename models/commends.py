from sqlalchemy import Column, Integer, String, DateTime, Float
from database import Base
from database import init_db


class Commends(Base):
    __tablename__ = 'googleCommends'
    id = Column(Integer, primary_key=True)
    title = Column(String(250))
    rating = Column(Float(10))
    ratingCount = Column(Integer)
    authorName = Column(String(250))
    # Date = Column(String(250))
    authorRating = Column(Float(10))
    reviewContent = Column(String(250))
    link = Column(String(250))

    def __init__(self, data):
        self.title = data['title']
        self.rating = data['rating']
        self.ratingCount = data['ratingCount']
        self.authorName = data['authorName']
        # self.Date = data['Date']
        self.authorRating = data['authorRating']
        self.reviewContent = data['reviewContent']
        self.link = data['link']

    def __repr__(self):
        return "<TbTest('%d', '%s', '%s', '%s', '%s'>" % (self.id, str(self.title), self.authorName, self.authorRating, self.reviewContent)


init_db()

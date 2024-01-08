import datetime

from sqlalchemy import Column, DateTime, BigInteger, String, Integer

from bot.db.base import Base


class UserPrompt(Base):
    __tablename__ = "userprompt"
    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=False)
    user_id = Column(BigInteger)
    file_id = Column(String, unique=True)
    prompt = Column(String, default="Design logo for ")
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    score = Column(Integer, default=0)

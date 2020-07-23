from sqlalchemy import Column, Integer, String, Sequence, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import connector

class User(connector.Manager.Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    lastname = Column(String(50))
    username = Column(String(12))
    password = Column(String(12))

class Game(connector.Manager.Base):
    __tablename__ = 'games'
    id = Column(Integer, Sequence('game_id_seq'), primary_key=True)
    title = Column(String(100))
    category = Column(String(50))
    description = Column(String(500))
    trailer = Column(String(100))
    version = Column(String(50))
    company = Column(String(50))
    price = Column(Integer)
    quantity = Column(Integer)
    valoration = Column(Integer)

class Review(connector.Manager.Base):
    __tablename__ = 'review'
    id = Column(Integer, Sequence('review_id_seq'), primary_key=True)
    content = Column(String(500))
    write_on = Column(DateTime(timezone=True))
    valoration = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User, foreign_keys=[user_id])
    game_id = Column(Integer, ForeignKey('games.id'))
    game = relationship(Game, foreign_keys=[game_id])

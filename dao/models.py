# coding: utf-8

# sqlacodegen mysql+pymysql://root:@127.0.0.1:3306/words

from application import db
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, String, text,Enum
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

#Base = declarative_base()
#metadata = Base.metadata

Base = db.Model
metadata = Base.metadata


class User(Base):
    __tablename__ = 'user'

    id = Column(String(100), primary_key=True)
    name = Column(String(100), nullable=False)
    lasthotdate = Column(Date)
    count = Column(INTEGER(11), nullable=False, server_default=text("'10'"))

class Word(Base):
    __tablename__ = 'word'

    id = Column(INTEGER(11), nullable=False)
    word = Column(String(1), primary_key=True)
    pinyin = Column(String(10), nullable=False)
    level = Column(INTEGER(11), nullable=False)
    strokes = Column(INTEGER(11), nullable=False)
    radicals = Column(String(1), nullable=False)
    
    hotness=None
    planFlag=None
    tagFlag=None

class Record(Base):
    __tablename__ = 'record'

    rid = Column(INTEGER(11), primary_key=True)
    word = Column(ForeignKey('word.word'), nullable=False, index=True)
    uid = Column(ForeignKey('user.id'), nullable=False, index=True)
    time = Column(DateTime, nullable=False)
    tag = Column(INTEGER(11))
    date = Column(Date, nullable=False)
    _from = Column('from', Enum('query', 'plan', 'explore','review'), nullable=False)
    user = relationship('User')
    word1 = relationship('Word',backref=db.backref("Records", lazy=True))


class Lasthot(Base):
    __tablename__ = 'lasthot'

    uid = Column(ForeignKey('user.id'), primary_key=True, nullable=False)
    word = Column(ForeignKey('word.word'), primary_key=True, nullable=False, index=True)
    hotness = Column(Float, nullable=False)

    user = relationship('User',backref=db.backref("lastHots", lazy=True))
    word1 = relationship('Word',backref=db.backref("lastHots", lazy=True))

class Plan(Base):
    __tablename__ = 'plan'

    pid = Column(BIGINT(20), primary_key=True, index=True)
    uid = Column(ForeignKey('user.id'), nullable=False, index=True)
    word = Column(ForeignKey('word.word'), nullable=False, index=True)
    date = Column(Date, nullable=False)
    learned = Column(TINYINT(1), nullable=False)

    user = relationship('User')
    word1 = relationship('Word',backref=db.backref("plans", lazy=True))
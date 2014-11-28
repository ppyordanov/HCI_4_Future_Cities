from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

from werkzeug.security import generate_password_hash, \
    check_password_hash


class Weather(Base):
    __tablename__ = 'weather'
    weatherid = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(50))

    def __init__(self, type):
        self.type = type

    def __repr__(self):
        return '<Weather %r>' % (self.title)


class Achievement(Base):
    __tablename__ = 'achievement'
    achievementid = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50))
    description = Column(String(200))

    # achievements = relationship('user_achievement', backref='achievement', lazy='dynamic')

    def __init__(self, title, description):
        self.title = title
        self.description = description

    def __repr__(self):
        return '<Achievement %r>' % (self.title)


class Rank(Base):
    __tablename__ = 'rank'
    rankid = Column(Integer, primary_key=True, autoincrement=True)
    positiveVotes = Column(Integer, default=0)
    negativeVotes = Column(Integer, default=0)

    def __init__(self, positiveVotes, negativeVotes):
        self.positiveVotes = positiveVotes
        self.negativeVotes = negativeVotes

    def __repr__(self):
        return '<Rank %r>' % (self.rankid)


class User(Base):
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    __tablename__ = 'sys_user'
    userid = Column(String(50), primary_key=True)
    rankid = Column(Integer, ForeignKey('rank.rankid'))
    achievementid = Column(Integer, ForeignKey('achievement.achievementid'))
    password = Column(String)
    email = Column(String(50))
    avatar = Column(String(200), default="/static/images/a.jpg")
    points = Column(Integer)
    firstName = Column(String(50))
    lastName = Column(String(50))

    # photos = relationship('photo', backref='sys_user', lazy='dynamic')
    # achievements = relationship('user_achievement', backref='sys_user', lazy='dynamic')

    def __init__(self, userid=None, rankid=None, achievementid=None, password=None, email=None, avatar=None,
                 points=None, firstName=None, lastName=None):
        self.userid = userid
        self.rankid = rankid
        self.set_password(password)
        self.email = email
        self.avatar = avatar
        self.points = points
        self.firstName = firstName
        self.lastName = lastName
        self.achievementid = achievementid

    def __repr__(self):
        return '<User %r>' % (self.userid)

    def serialize(self):
        return {
            'userid': self.userid,
            'rankid': self.rankid,
            'achievementid': self.achievementid,
            'email': self.email,
            'avatar': self.avatar,
            'points': self.points,
            'firstName': self.firstName,
            'lastName': self.lastName
        }


class Photo(Base):
    __tablename__ = 'photo'
    photoid = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(String, ForeignKey('sys_user.userid'))
    rankid = Column(String, ForeignKey('rank.rankid'))
    title = Column(String(50))
    description = Column(String(200))
    photo = Column(String(200))
    square = Column(Integer)
    type = Column(String(4))
    weather = Column(String)

    def __init__(self, title, userid, rankid, description, photo, square, type, weather):
        self.title = title
        self.rankid = rankid
        self.description = description
        self.photo = photo
        self.square = square
        self.type = type
        self.userid = userid
        self.weather = weather

    def __repr__(self):
        return '<Photo %r>' % (self.title)

    def serialize(self):
        return {
            'title': self.title,
            'rankid': self.rankid,
            'description': self.description,
            'photo': self.photo,
            'square': self.square,
            'type': self.type,
            'userid': self.userid,
            'weather': self.weather
        }


class User_Achievement(Base):
    __tablename__ = 'user_achievement'
    uaid = Column(Integer, primary_key=True, autoincrement=True)
    achievementid = Column(Integer, ForeignKey('achievement.achievementid'))
    userid = Column(Integer, ForeignKey('sys_user.userid'))

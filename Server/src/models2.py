from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Achievement(Base):
    __tablename__ = 'achievement'

    achievementid = Column(Integer, primary_key=True)
    title = Column(String(50))
    description = Column(String(200))


class Photo(Base):
    __tablename__ = 'photo'

    photoid = Column(Integer, primary_key=True)
    userid = Column(ForeignKey(u'sys_user.userid'))
    rankid = Column(ForeignKey(u'rank.rankid'))
    title = Column(String(50))
    description = Column(String(200))
    photo = Column(String(200))
    square = Column(Integer)
    type = Column(String(4))

    rank = relationship(u'Rank')
    sys_user = relationship(u'SysUser')


class Rank(Base):
    __tablename__ = 'rank'

    rankid = Column(Integer, primary_key=True)
    positiveVotes = Column(Integer)
    negativeVotes = Column(Integer)


class SysUser(Base):
    __tablename__ = 'sys_user'

    userid = Column(String(50), primary_key=True)
    rankid = Column(ForeignKey(u'rank.rankid'))
    achievementid = Column(ForeignKey(u'achievement.achievementid'))
    password = Column(String)
    email = Column(String(50))
    avatar = Column(String(200))
    points = Column(Integer)
    firstName = Column(String(50))
    lastName = Column(String(50))

    achievement = relationship(u'Achievement')
    rank = relationship(u'Rank')


class UserAchievement(Base):
    __tablename__ = 'user_achievement'

    uaid = Column(Integer, primary_key=True)
    achievementid = Column(ForeignKey(u'achievement.achievementid'))
    userid = Column(ForeignKey(u'sys_user.userid'))

    achievement = relationship(u'Achievement')
    sys_user = relationship(u'SysUser')


class Weather(Base):
    __tablename__ = 'weather'

    weatherid = Column(Integer, primary_key=True)
    type = Column(String(50))
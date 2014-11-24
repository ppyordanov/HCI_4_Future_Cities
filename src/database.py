from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///DB/sg.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    from models import User, Photo
    Base.metadata.create_all(bind=engine)


#deprecated API version engine from previous version of the web application
def getall_users():

    users =Base.query('select * from sys_user ')
    return users

def getone_user(userid):
    user = Base.query('select * from sys_user where userid = ?',
        [userid,], one=True)
    if user is None:
        return 'No such user'

    return user

def getall_photos():

    photos = Base.query('select * from photo ')
    return photos

def getall_type_photos(type):

    photos = Base.query('select * from photo where type = ?', [type], one=True)
    return photos

def getone_photo_location(square):
    photo = Base.query('select photo from photo where square = ?',
        [square], one=True)
    if photo is None:
        return 'No such photo'

    return photo.itervalues().next()



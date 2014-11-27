from database import *
from models import *


def db_population():
    db_session.add(Weather("Rainy"))
    db_session.add(Weather("Sunny"))
    db_session.add(Weather("Snowy"))
    db_session.add(Weather("Windy"))

    db_session.commit()

    db_session.add(Achievement("rainbow", "rainbow on rainy photo"))
    db_session.add(Achievement("rain and sun", "sunny and rainy weather"))

    db_session.commit()

    db_session.add(Rank(87, 9))
    db_session.add(Rank(100, 12))
    db_session.add(Rank(10, 100))
    db_session.add(Rank(50, 50))
    db_session.add(Rank(0, 0))
    db_session.add(Rank(1, 1))

    db_session.commit()
    db_session.add(User('admin', 'SuperUser', 0, 'pass1', 'email1', '/static/images/a.jpg', 11, 'Tom', 'Robertson'))
    db_session.add(User('user1', 'Regular', 0, 'pass1', 'email1', '/static/images/a.jpg', 11, 'Tom', 'Robertson'))
    db_session.add(User('user2', 'Regular', 1, 'pass1', 'email2', '/static/images/a.jpg', 100, 'Tom', 'Robertson'))
    db_session.add(User('user3', 'Regular', 0, 'pass1', 'email3', '/static/images/a.jpg', 50, 'John', 'Wilson'))
    db_session.add(User('user4', 'Regular', 1, 'pass1', 'email4','/static/images/a.jpg', 20, 'Bay', 'Kenish'))
    db_session.add(User('user5', 'Regular', 0, 'pass1', 'email5', '/static/images/a.jpg', 1000, 'Vasko', 'Dimitrov'))

    db_session.commit()

    # bad weather
    db_session.add(Photo('Glasgow scenery', 'admin', 0, 'bad weather', '/static/images/user_data/bad/295.jpg', 295, 'bad', 'Cloudy'))
    db_session.add(Photo('Glasgow scenery', 'admin', 1, 'bad weather', '/static/images/user_data/bad/296.jpg', 296, 'bad', 'Rainy'))
    db_session.add(Photo('Glasgow scenery', 'admin', 2, 'bad weather', '/static/images/user_data/bad/297.jpg', 297, 'bad', 'Cloudy'))
    db_session.add(Photo('Glasgow scenery', 'admin', 3, 'bad weather', '/static/images/user_data/bad/298.jpg', 298, 'bad', 'Rainy'))
    db_session.add(Photo('Glasgow scenery', 'admin', 3, 'bad weather', '/static/images/user_data/bad/335.jpg', 335, 'bad', 'Cloudy'))
    db_session.add(Photo('Glasgow scenery', 'admin', 4, 'bad weather', '/static/images/user_data/bad/337.jpg', 337, 'bad', 'Rainy'))
    db_session.add(Photo('Glasgow scenery', 'admin', 1, 'bad weather', '/static/images/user_data/bad/338.jpg', 338, 'bad', 'Cloudy'))
    db_session.add(Photo('Glasgow scenery', 'admin', 5, 'bad weather', '/static/images/user_data/bad/339.jpg', 339, 'bad', 'Rainy'))
    db_session.add(Photo('Glasgow scenery', 'admin', 2, 'bad weather', '/static/images/user_data/bad/377.jpg', 377, 'bad', 'Cloudy'))
    db_session.add(Photo('Glasgow scenery', 'admin', 3, 'bad weather', '/static/images/user_data/bad/378.jpg', 378, 'bad', 'Rainy'))
    db_session.add(Photo('Glasgow scenery', 'admin', 2, 'bad weather', '/static/images/user_data/bad/379.jpg', 379, 'bad', 'Cloudy'))

    #good weather
    db_session.add(Photo('Glasgow scenery', 'admin', 1, 'good weather', '/static/images/user_data/good/295.jpg', 295, 'good', 'Sunny'))
    db_session.add(Photo('Glasgow scenery', 'admin', 3, 'good weather', '/static/images/user_data/good/296.jpg', 296, 'good', 'Sunny, Cloudy'))
    db_session.add(Photo('Glasgow scenery', 'admin', 3, 'good weather', '/static/images/user_data/good/297.jpg', 297, 'good', 'Sunny'))
    db_session.add(Photo('Glasgow scenery', 'admin', 4, 'good weather', '/static/images/user_data/good/298.jpg', 298, 'good', 'Sunny, Cloudy'))
    db_session.add(Photo('Glasgow scenery', 'admin', 5, 'good weather', '/static/images/user_data/good/335.jpg', 335, 'good', 'Sunny'))
    db_session.add(Photo('Glasgow scenery', 'admin', 1, 'good weather', '/static/images/user_data/good/337.jpg', 337, 'good', 'Sunny, Cloudy'))
    db_session.add(Photo('Glasgow scenery', 'admin', 2, 'good weather', '/static/images/user_data/good/338.jpg', 338, 'good', 'Sunny'))
    db_session.add(Photo('Glasgow scenery', 'admin', 3, 'good weather', '/static/images/user_data/good/339.jpg', 339, 'good', 'Sunny'))
    db_session.add(Photo('Glasgow scenery', 'admin', 4, 'good weather', '/static/images/user_data/good/377.jpg', 377, 'good', 'Sunny, Cloudy'))
    db_session.add(Photo('Glasgow scenery', 'admin', 1, 'good weather', '/static/images/user_data/good/378.jpg', 378, 'good', 'Sunny'))
    db_session.add(Photo('Glasgow scenery', 'admin', 2, 'good weather', '/static/images/user_data/good/379.jpg', 379, 'good', 'Sunny, Cloudy'))

    db_session.commit()
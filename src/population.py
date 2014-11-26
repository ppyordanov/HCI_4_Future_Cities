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

    db_session.add(User('user1', 0, 0, 'pass1', 'email1', None, 11, 'Tom', 'Robertson'))
    db_session.add(User('user2', 1, 1, 'pass1', 'email2', None, 100, 'Tom', 'Robertson'))
    db_session.add(User('user3', 2, 0, 'pass1', 'email3', None, 50, 'John', 'Wilson'))
    db_session.add(User('user4', 3, 1, 'pass1', 'email4', None, 20, 'Bay', 'Kenish'))
    db_session.add(User('user5', 4, 0, 'pass1', 'email5', None, 1000, 'Vasko', 'Dimitrov'))

    db_session.commit()

    # bad weather
    db_session.add(Photo('Glasgow scenery', 0, 0, 'bad weather', '/static/images/user_data/bad/295.jpg', 295, 'bad'))
    db_session.add(Photo('Glasgow scenery', 0, 1, 'bad weather', '/static/images/user_data/bad/296.jpg', 296, 'bad'))
    db_session.add(Photo('Glasgow scenery', 0, 2, 'bad weather', '/static/images/user_data/bad/297.jpg', 297, 'bad'))
    db_session.add(Photo('Glasgow scenery', 0, 3, 'bad weather', '/static/images/user_data/bad/298.jpg', 298, 'bad'))
    db_session.add(Photo('Glasgow scenery', 0, 3, 'bad weather', '/static/images/user_data/bad/335.jpg', 335, 'bad'))
    db_session.add(Photo('Glasgow scenery', 0, 4, 'bad weather', '/static/images/user_data/bad/337.jpg', 337, 'bad'))
    db_session.add(Photo('Glasgow scenery', 0, 1, 'bad weather', '/static/images/user_data/bad/338.jpg', 338, 'bad'))
    db_session.add(Photo('Glasgow scenery', 0, 5, 'bad weather', '/static/images/user_data/bad/339.jpg', 339, 'bad'))
    db_session.add(Photo('Glasgow scenery', 0, 2, 'bad weather', '/static/images/user_data/bad/377.jpg', 377, 'bad'))
    db_session.add(Photo('Glasgow scenery', 0, 3, 'bad weather', '/static/images/user_data/bad/378.jpg', 378, 'bad'))
    db_session.add(Photo('Glasgow scenery', 0, 2, 'bad weather', '/static/images/user_data/bad/379.jpg', 379, 'bad'))

    #good weather
    db_session.add(Photo('Glasgow scenery', 4, 1, 'good weather', '/static/images/user_data/good/295.jpg', 295, 'good'))
    db_session.add(Photo('Glasgow scenery', 3, 3, 'good weather', '/static/images/user_data/good/296.jpg', 296, 'good'))
    db_session.add(Photo('Glasgow scenery', 2, 3, 'good weather', '/static/images/user_data/good/297.jpg', 297, 'good'))
    db_session.add(Photo('Glasgow scenery', 1, 4, 'good weather', '/static/images/user_data/good/298.jpg', 298, 'good'))
    db_session.add(Photo('Glasgow scenery', 4, 5, 'good weather', '/static/images/user_data/good/335.jpg', 335, 'good'))
    db_session.add(Photo('Glasgow scenery', 1, 1, 'good weather', '/static/images/user_data/good/337.jpg', 337, 'good'))
    db_session.add(Photo('Glasgow scenery', 2, 2, 'good weather', '/static/images/user_data/good/338.jpg', 338, 'good'))
    db_session.add(Photo('Glasgow scenery', 4, 3, 'good weather', '/static/images/user_data/good/339.jpg', 339, 'good'))
    db_session.add(Photo('Glasgow scenery', 2, 4, 'good weather', '/static/images/user_data/good/377.jpg', 377, 'good'))
    db_session.add(Photo('Glasgow scenery', 0, 1, 'good weather', '/static/images/user_data/good/378.jpg', 378, 'good'))
    db_session.add(Photo('Glasgow scenery', 0, 2, 'good weather', '/static/images/user_data/good/379.jpg', 379, 'good'))

    db_session.commit()
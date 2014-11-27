import base64
import contextlib
import sqlite3
import os

from flask.ext.login import *
from flask import session, g, abort, render_template, flash, jsonify
from flask import Flask, redirect, url_for
from flask import request
from werkzeug.utils import secure_filename

from register import RegistrationForm
from database import *
from models import User, Photo
from population import db_population
from upload import UploadForm


UPLOAD_FOLDER = 'static/images/user_data/'
ALLOWED_EXTENSIONS = set(['jpg'])

# configuration
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
DATABASE = os.path.join(PROJECT_ROOT, 'DB', 'sg.db')
SCHEMA = os.path.join(PROJECT_ROOT, 'DB', 'schema.sql')
POPULATION = os.path.join(PROJECT_ROOT, 'DB', 'population_script.sql')
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'



# application
app = Flask(__name__)
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(PROJECT_ROOT, UPLOAD_FOLDER)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


con = engine.connect()

login_manager = LoginManager()
login_manager.init_app(app)

# Session DATA
USER_SESSION = {}
GOOD = ['sunny', 'hot', 'cloudy']
BAD = ['windy', 'rainy', 'snowy' ,'hail']


@login_manager.user_loader
def load_user(userid):
    return


'''
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource(SCHEMA, mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
'''

#setup		
@app.before_request
def before_request():
    init_db()
    #db_population()
    #g.db = connect_db()


'''
#populate
def populate_db():
    with closing(connect_db()) as db:
        with app.open_resource(POPULATION, mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
'''


@app.teardown_appcontext
def shutdown_session(exception=None):
    USER_SESSION = {}  #empty session dictionary
    db_session.remove()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def getUserPoints(UNAME):
    return User.query.filter_by(userid=UNAME).first().points


def getUserPhotos(UNAME):
    return Photo.query.filter_by(userid=UNAME)

def getUser(UNAME):
    return User.query.filter_by(userid=UNAME).first()

def photoNum():
    return len(Photo.query.all())


#views
@app.route("/")
def home():
    #user_list = [user.serialize for user in User.query.all()]
    photo_list = [photo.serialize() for photo in Photo.query.all()]
    user = getUser(USERNAME)
    ps = photoNum()

    return render_template('home.html', photo_list=photo_list, user=user, ps=ps)


#RESTful API for DEMO
@app.route("/get_photos", methods=['GET'])
def get_photos():
    if request.method == 'GET':
        list = [photo.serialize() for photo in Photo.query.all()]
        return jsonify(results=list)


@app.route("/get_users", methods=['GET'])
def get_users():
    if request.method == 'GET':
        list = [user.serialize() for user in User.query.all()]
        return jsonify(results=list)


@app.route("/upload")
def upload():
    user = getUser(USERNAME)
    form = UploadForm()
    ps = photoNum()
    return render_template('upload.html', type='Upload', user=user, form=form, ps=ps)


@app.route("/update")
def update():
    user = getUser(USERNAME)
    form = UploadForm()
    ps = photoNum()
    return render_template('upload.html', type='Update', user=user, form=form, ps=ps)


@app.route('/upload_photo', methods=('GET', 'POST'))
def upload_photo():
    user = getUser(USERNAME)
    points = getUserPoints(USERNAME)
    form = UploadForm(request.form)
    ps = photoNum()
    if request.method == 'POST'  and form.validate():
        file = request.files['file']
        if file and allowed_file(file.filename):
            action = request.form['action']
            square = form.square.data
            title = form.title.data
            description = form.description.data
            weather = form.weather.data
            type = None
            if(weather in GOOD):
                type = 'good'
            else:
                type ='bad'
            parsename = str(square) + '.jpg'
            filename = secure_filename(parsename)
            path = UPLOAD_FOLDER + "/" + type + "/" + filename
            file.save(path)
            photo = Photo(title, user.userid, 0, description, path, square,type,weather)
            db_session.add(photo)
            if action=='Upload':
                flash('+50 POINTS. The new photo was successfully posted.')
                points +=50
            elif action=='Update':
                flash('+20 POINTS. The new photo was successfully updated.')
                points +=20
            db_session.query(User).filter_by(userid=USERNAME).update({'points': points})
            db_session.commit()
        return redirect(url_for('home'))
    return render_template('upload.html', points=points, user=user, form=form, ps=ps)


#No encrypted verification - demonstation purposes
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    ps = photoNum()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username != app.config['USERNAME']:
            error = 'Invalid username'
        elif password != app.config['PASSWORD']:
            error = 'Invalid password. Please try again!'
        else:
            session['logged_in'] = True
            session['user_id'] = username
            USER_SESSION['id'] = username
            flash('You were successfully logged in.')
            return redirect(url_for('home'))

    return render_template('login.html', error=error, ps=ps)


'''
    form = LoginForm()
    if form.validate_on_submit():
        flash(u'Successfully logged in as %s' % form.user.username)
        session['userid'] = form.user.id
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

'''


@app.route('/register', methods=['GET', 'POST'])
def register():
    ps = photoNum()
    form = RegistrationForm(request.form)
    return render_template('register.html', form=form, ps=ps)


@app.route('/register_submit', methods=['GET', 'POST'])
def register_submit():
    if request.method == 'POST':
        user = User(request.form['username'], 0, 1, request.form['password'], request.form['email'], None, 100,
                    'william', 'shot')
        db_session.add(user)
        db_session.commit()
        flash('Your registration was successful.')
        return redirect(url_for('login'))
    return


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You have been logged out successfully.')
    return redirect(url_for('home'))


@app.route('/statistics')
def statistics():
    ps = photoNum()
    user = getUser(USERNAME)
    uphotos = getUserPhotos(USERNAME)
    return render_template('statistics.html', user=user, photos=uphotos, ps=ps)


@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        abort(401)
    ps = photoNum()
    user = getUser(USERNAME)
    flash('Welcome, ' + user.userid + '.')
    good_photos = []
    users = User.query.all()
    photos = Photo.query.all()
    return render_template('dashboard.html', good_photos=good_photos, users=users, photos=photos, user=user, ps=ps)


#DB querying

def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


#Truncate database on teardown
def truncate():
    with contextlib.closing(engine.connect()) as con:
        trans = con.begin()
        for table in reversed(Base.metadata.sorted_tables):
            con.execute(table.delete())
        trans.commit()


#run application
if __name__ == "__main__":
    app.run()
	

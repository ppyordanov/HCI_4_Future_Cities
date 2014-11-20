import contextlib
import sqlite3
import os
from flask.ext.login import *
from flask import session, g, abort, render_template, flash
from flask import Flask, redirect, url_for
import sqlalchemy
from flask import request
from werkzeug.utils import secure_filename
from register import RegistrationForm
from login import LoginForm
from login import *

from population import db_population
from database import *
from models import User, Photo


UPLOAD_FOLDER = 'static/images/user_data/'
ALLOWED_EXTENSIONS = set(['jpg'])

# configuration
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
DATABASE = os.path.join(PROJECT_ROOT, 'DB', 'sg2.db')
SCHEMA = os.path.join(PROJECT_ROOT, 'DB', 'schema.sql')
POPULATION = os.path.join(PROJECT_ROOT, 'DB', 'population_script.sql')
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'



#application
app = Flask(__name__)
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(PROJECT_ROOT, UPLOAD_FOLDER)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])




login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
    return User.get(userid)

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
    db_population()
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
    truncate()
    db_session.remove()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

#views
@app.route("/")
def home():
    return render_template('home.html')


@app.route("/update")
def update():
    return


@app.route("/upload")
def upload():
    return render_template('upload.html')
    #return render_template('upload.html')

@app.route('/upload_photo', methods=['POST'])
def upload_photo():

    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            TYPE = request.form['type']
            path = os.path.join(app.config['UPLOAD_FOLDER'], request.form['type'], filename)
            file.save(path)
            photo = Photo(0, 'admin', request.form['title'], request.form['description'],path, request.form['square'], TYPE )
            db_session.add(photo)
            db_session.commit()
            flash('New photo was successfully posted')
            return redirect(url_for('home'))
    return



	
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

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
    form = RegistrationForm(request.form)
    return render_template('register.html', form=form)

@app.route('/register_submit', methods=['GET', 'POST'])
def register_submit():

    if request.method == 'POST':
        user = User(request.form['username'],0,1,request.form['password'], request.form['username'],None,100,'william','shot')
        db_session.add(user)
        db_session.commit()
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return

	
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('home'))

@app.route('/statistics')
def statistics():
    return render_template('statistics.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        abort(401)
    flash('personal dashboard')
    good_photos = []
    users = len(User.query.all())
    photos =len(Photo.query.all())
    return render_template('dashboard.html', good_photos=good_photos, users=users, photos=photos)


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
	

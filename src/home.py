import sqlite3
import os
from contextlib import closing

from flask import session, g, abort, render_template, flash
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = '/static/images/user_data/'
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

#application
app = Flask(__name__)
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])
	
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource(SCHEMA, mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

#setup		
@app.before_request
def before_request():
    g.db = connect_db()

#populate
def populate_db():
    with closing(connect_db()) as db:
        with app.open_resource(POPULATION, mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

#views
@app.route("/")
def home():
    cur = g.db.execute('select * from photo')
    photos = [dict(photoID=row[0],userID=row[1], rankID=row[2],time=row[3],latitude=row[4],longitude=row[5],title=row[6],description=row[7], square=row[9]) for row in cur.fetchall()]
    return render_template('home.html', photos = photos)


@app.route("/update")
def update():
    return


@app.route("/upload")
def upload():
    return render_template('upload.html')

@app.route('/upload_photo', methods=['POST'])
def upload_photo():


    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)

            g.db.execute('insert into photo(userID, rankID, time, latitude, longitude, title, description, photo, square) values (admin, 1, null, 0.0, 0.0, ?, ?, ?, ?);',
                         [request.form['title'], request.form['description'],save_path,request.form['square']])
            g.db.commit()

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
	
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        abort(401)
    flash('personal dashboard')
    return render_template('dashboard.html')


#DB querying

def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


def getall_users():

    users = query_db('select * from sys_user ')
    return users

def getone_user(userid):
    user = query_db('select * from users where userid = ?',
                userid, one=True)
    if user is None:
        return 'No such user'

    return user

def getall_photos():

    photos = query_db('select * from photos ')
    return photos

def getone_photo(photoid):
    photo = query_db('select * from photos where photoid = ?',
                id, one=True)
    if photo is None:
        return 'No such photo'

    return photo



	
#run application
if __name__ == "__main__":
    init_db()
    populate_db()
    app.run()
	

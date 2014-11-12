import sqlite3
import os
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

# configuration
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
DATABASE = os.path.join(PROJECT_ROOT, 'DB', 'sg.db')
SCHEMA = os.path.join(PROJECT_ROOT, 'DB', 'schema.sql')
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

#application
app = Flask(__name__)
app.config.from_object(__name__)

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

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
		
#views
@app.route("/")
def home():
    cur = g.db.execute('select * from photo')
    photos = [dict(photoID=row[0],userID=row[1], rankID=row[2],time=row[3],latitude=row[4],longitude=row[5],title=row[6],description=row[7]) for row in cur.fetchall()]
    return render_template('show_entries.html', photos = photos)
	
@app.route('/upload', methods=['POST'])
def upload_photo():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into photo(userID, rankID, time, latitude, longitude, title, description) values (null, null, null, 0.0, 0.0, ?, ?);',
                 [request.form['title'], request.form['description']])
    g.db.commit()
    flash('New photo was successfully posted')
    return redirect(url_for('home'))
	
	
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
	
	
#run application
if __name__ == "__main__":
    app.run()
	

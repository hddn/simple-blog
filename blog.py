import os
import sqlite3
from datetime import datetime
from flask import (Flask, request, session, g, redirect,
                   url_for, abort, render_template, flash)
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from img_resizer import edit_image
from PIL import Image


app = Flask(__name__)
app.config.from_object(__name__)

APP_ROOT = os.path.realpath(os.path.dirname(__file__))
ALLOWED_FILES = set(['png', 'gif', 'jpg', 'jpeg', 'mp3'])
PIC_EXTENSIONS = set(['png', 'gif', 'jpg', 'jpeg'])

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, '..', 'blog.db'),
    SECRET_KEY='very_secret_key',
    USERNAME='admin',
    PASSWORD='pbkdf2:sha1:1000$fQPAbL6Y$74fac58d9b19e991e46ac5d4e52db7402556843b'
    ))


def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'],
                         detect_types=sqlite3.PARSE_DECLTYPES)
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    init_db()
    print 'Initialized the database.'


def check_password(password, hashed_pass=app.config['PASSWORD']):
    return check_password_hash(hashed_pass, password)


@app.route('/')
def show_posts():
    db = get_db()
    ordering = request.args.get('order_by_date')
    if not ordering or ordering == '1':
        cur = db.execute('select title, preview, created, id '
                         'from posts where archived = 0 order by created desc')
    else:
        cur = db.execute('select title, preview, created, id '
                         'from posts where archived = 0 order by created ')
    posts = cur.fetchall()
    return render_template('index.html', posts=posts)


@app.route('/archive')
def archive():
    db = get_db()
    ordering = request.args.get('order_by_date')
    if not ordering or ordering == '1':
        cur = db.execute('select title, preview, created, id '
                         'from posts where archived = 1 order by created desc')
    else:
        cur = db.execute('select title, preview, created, id '
                         'from posts where archived = 1 order by created')
    posts = cur.fetchall()
    return render_template('index.html', posts=posts)


@app.route('/view_post/<id>', methods=['GET', 'POST'])
def view_post(id):
    if request.method == 'POST':
        if not session.get('logged_in'):
            abort(401)

        db = get_db()
        db.execute('update posts set archived = 1 where id = {}'.format(id))
        db.commit()
        flash('Post was moved to archive', 'success')
        return redirect(url_for('show_posts'))
    db = get_db()
    cur = db.execute('select title, content, created, id '
                     'from posts where id = {}'.format(id))
    posts = cur.fetchall()
    return render_template('view_post.html', posts=posts)


@app.route('/add', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        if not session.get('logged_in'):
            abort(401)
        db = get_db()
        content = request.form['preview'] + request.form['content']
        db.execute('insert into posts '
                   '(title, preview, content, created, archived) '
                   'values (?, ?, ?, ?, ?)',
                   [request.form['title'],
                    request.form['preview'],
                    content,
                    datetime.now(),
                    0])
        db.commit()
        flash('New post was successfully posted', 'success')
        return redirect(url_for('show_posts'))
    return render_template('add_post.html')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_FILES


@app.route('/upload', methods=['POST'])
def upload_file():
    path = os.path.join(APP_ROOT, 'static', 'uploads')
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            flash('No file selected!', 'warning')
            return redirect(url_for('add_post'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if filename.rsplit('.', 1)[1] != 'mp3':
                edit_image(file, filename)
            else:
                file.save(os.path.join(path, filename))
    return redirect(url_for('add_post'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif not check_password(request.form['password']):
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in', 'success')
            return redirect(url_for('show_posts'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out', 'warning')
    return redirect(url_for('show_posts'))


if __name__ == '__main__':
    app.debug = False
    import logging
    from logging.handlers import RotatingFileHandler
    logger = logging.getLogger('werkzeug')
    file_handler = RotatingFileHandler('blog.log',
                                       maxBytes=1024 * 1024 * 10,
                                       backupCount=10)
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'
                                  ' - [in %(pathname)s:%(lineno)d]')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    app.run()

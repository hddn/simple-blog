import os
import sqlite3
from datetime import datetime
from flask import (Flask, request, session, g, redirect, 
                   url_for, abort, render_template, flash)


app = Flask(__name__)
app.config.from_object(__name__)


app.config.update(dict(
    DATABASE=os.path.join(app.root_path, '..', 'blog.db'),    
    SECRET_KEY='very_secret_key',
    USERNAME='admin',
    PASSWORD='admin'
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

import os
import sqlite3
from datetime import datetime
from flask import (Flask, request, session, g, redirect, 
                   url_for, abort, render_template, flash)


app = Flask(__name__)
app.config.from_object(__name__)


app.config.update(dict(
    DATABASE=os.path.join(app.root_path, '..', 'blog.db'),
    DEBUG=True,
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
    cur = db.execute('select title, content, created from posts order by id desc')
    posts = cur.fetchall()
    return render_template('index.html', posts=posts)


@app.route('/add', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        if not session.get('logged_in'):
            abort(401)
        db = get_db()
        db.execute('insert into posts (title, content, created) values (?, ?, ?)',
                   [request.form['title'], request.form['content'], datetime.now()])
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
    app.run()

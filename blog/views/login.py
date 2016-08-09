from flask import (request, session, redirect,
                   url_for, render_template, flash)

from ..config import USERNAME
from ..util import check_password
from .. import app


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != USERNAME:
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

from flask import (request, session, redirect,
                   url_for, render_template, flash)
from flask.views import MethodView

from ..config import USERNAME, PASSWORD
from ..util import check_password


class LoginView(MethodView):

    def get(self, error=None):
        return render_template('login.html', error=error)

    def post(self):
        error = None
        if request.form['username'] != USERNAME:
            error = 'Invalid username'
        elif not check_password(request.form['password'], PASSWORD):
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in', 'success')
            return redirect(url_for('show_posts'))
        return self.get(error)

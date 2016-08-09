from flask import (session, request, render_template,
                   redirect, flash, abort, url_for)
from flask.views import MethodView
from datetime import datetime

from ..db import get_db


class PostCreateView(MethodView):

    def get(self):
        return render_template('add_post.html')

    def post(self):
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

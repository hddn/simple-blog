from flask import (session, request, render_template,
                   redirect, flash, abort, url_for)
from flask.views import MethodView
from ..db import get_db


class PostView(MethodView):

    def get(self, id):
        db = get_db()
        cur = db.execute('select title, content, created, id '
                         'from posts where id = {}'.format(id))
        posts = cur.fetchall()
        return render_template('view_post.html', posts=posts)

    def post(self, id):
        if not session.get('logged_in'):
            abort(401)

        db = get_db()
        db.execute('update posts set archived = 1 where id = {}'.format(id))
        db.commit()
        flash('Post was moved to archive', 'success')
        return redirect(url_for('show_posts'))

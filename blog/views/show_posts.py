from flask import request
from template_view import TemplateView
from ..db import get_db


class PostsView(TemplateView):

    def get_template_name(self):
        return 'index.html'

    def get_context(self):
        db = get_db()
        ordering = request.args.get('order_by_date')
        if request.path == '/archive':
            archived = 1
        else:
            archived = 0
        if not ordering or ordering == '1':
            cur = db.execute('select title, preview, created, id '
                             'from posts where archived = {} '
                             'order by created desc'.format(archived))
        else:
            cur = db.execute('select title, preview, created, id '
                             'from posts where archived = {} '
                             'order by created'.format(archived))
        context = cur.fetchall()
        return context

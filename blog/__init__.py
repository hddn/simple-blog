from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

from views import (PostCreateView, PostView, PostsView,
                   UploadFileView, LoginView, LogoutView)
from util import log_errors


app.add_url_rule('/',
                 view_func=log_errors(PostsView.as_view('show_posts')))
app.add_url_rule('/archive',
                 view_func=log_errors(PostsView.as_view('archive')))
app.add_url_rule('/view_post/<id>',
                 view_func=log_errors(PostView.as_view('view_post')))
app.add_url_rule('/add',
                 view_func=log_errors(PostCreateView.as_view('add_post')))
app.add_url_rule('/upload',
                 view_func=log_errors(UploadFileView.as_view('upload_file')))
app.add_url_rule('/login',
                 view_func=log_errors(LoginView.as_view('login')))
app.add_url_rule('/logout',
                 view_func=log_errors(LogoutView.as_view('logout')))

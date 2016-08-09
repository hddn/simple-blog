import os


CSRF_ENABLED = True
ROOT = os.path.realpath(os.path.dirname(__file__))
APP_ROOT = os.path.join(ROOT, 'blog')

DATABASE = os.path.join(ROOT, '..', 'blog.db')
SECRET_KEY = 'very_secret_key'
USERNAME = 'admin'
PASSWORD = 'pbkdf2:sha1:1000$fQPAbL6Y$74fac58d9b19e991e46ac5d4e52db7402556843b'

ALLOWED_FILES = set(['png', 'gif', 'jpg', 'jpeg', 'mp3'])
PIC_EXTENSIONS = set(['png', 'gif', 'jpg', 'jpeg'])

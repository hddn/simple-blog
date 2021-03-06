import logging
from logging.handlers import RotatingFileHandler
from functools import wraps

from werkzeug.security import check_password_hash, generate_password_hash


def hash_password(password):
    return generate_password_hash(password)


def check_password(password, hashed_pass):
    return check_password_hash(hashed_pass, password)


def allowed_file(filename, allowed_files):
    return '.' in filename and filename.rsplit('.', 1)[1] in allowed_files


def logger():
    logger = logging.getLogger('werkzeug')
    file_handler = RotatingFileHandler('blog.log',
                                       maxBytes=1024 * 1024 * 10,
                                       backupCount=10)
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'
                                  ' - [in %(pathname)s:%(lineno)d]')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


def log_errors(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception, e:
            log = logger()
            log.exception(e)
    return wrapper

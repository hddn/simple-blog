import os
import ConfigParser

from ..util import hash_password


root = os.path.realpath(os.path.dirname(__file__))
config_path = os.path.join(root, 'config.ini')
config = ConfigParser.ConfigParser()
config.read(config_path)

APPLICATION_ROOT = config.get('PATHS', 'app_root')
DATABASE = config.get('PATHS', 'db')
SECRET_KEY = config.get('SECRETS', 'key')
USERNAME = config.get('SECRETS', 'username')
PASSWORD = hash_password(config.get('SECRETS', 'password'))

ALLOWED_FILES = set(['png', 'gif', 'jpg', 'jpeg', 'mp3'])
PIC_EXTENSIONS = set(['png', 'gif', 'jpg', 'jpeg'])

from blog import app
from blog.util import logger


if __name__ == '__main__':
    app.debug = False
    logger()
    app.run()

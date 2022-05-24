import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # ...
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    PLIVO_AUTH_ID = os.getenv('PLIVO_AUTH_ID')
    PLIVO_AUTH_TOKEN = os.getenv('PLIVO_AUTH_TOKEN')
    PLIVO_NUMBER = os.getenv('PLIVO_NUMBER')
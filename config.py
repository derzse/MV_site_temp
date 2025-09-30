import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Language configuration
    LANGUAGES = {
    'en': 'English',
    'ro': 'Română'
    }
    BABEL_DEFAULT_LOCALE = 'ro'
    BABEL_DEFAULT_TIMEZONE = 'UTC'
    BABEL_TRANSLATION_DIRECTORIES = os.path.join(basedir, 'translations')  # Fixed
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Construim viitorul, circuit dupa circuit.'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
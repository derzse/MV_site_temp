from config import Config
import os
from flask import Flask
from flask_babel import Babel, _, get_locale, gettext, ngettext

from utils.seo import LanguageAwareSEOTitleManager
from .extensions import db, seo_manager
from .main import main as main_blueprint
from utils.locale import get_locale
# from .posts import posts as posts_blueprint
# from .questions import questions as questions_blueprint

def create_app(config_class=Config):
    """Create a Flask application.
    
    Args:
        config_class: The configuration class to use.
    
    Returns:
        A Flask application instance.
    """
    # Create and configure the app
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    
    # Load the configuration
    app.config.from_object(config_class)
    
    # Debugging lines to check if the config is loaded correctly
    # print(app.config['SECRET_KEY'])  # Debugging line to check if the config is loaded
    # print(app.config['LANGUAGES'])    # Debugging line to check if the config is loaded
    # print(app.config['BABEL_DEFAULT_LOCALE'])  # Debugging line to check if the config is loaded
    # print(app.config['BABEL_DEFAULT_TIMEZONE'])  # Debugging line to check if the config is loaded
    # print(app.config['BABEL_TRANSLATION_DIRECTORIES'])  # Debugging line to check if the config is loaded
    # print(app.secret_key)  # Debugging line to check if the secret key is set
    
    # Ensure the instance folder exists
    try:
        # Create the instance folder if it doesn't exist
        os.makedirs(app.instance_path)
    except OSError:
        # If the instance folder already exists, print a message
        print("Instance folder already exists.")
        pass

    # Initialize extensions
    db.init_app(app)
      
    # Initialize Babel with the locale selector function (Flask-Babel 4.0.0 style)
    babel = Babel(app, locale_selector=get_locale)

    # Register blueprints
    app.register_blueprint(main_blueprint)
    # app.register_blueprint(posts_blueprint, url_prefix='/posts')
    # app.register_blueprint(questions_blueprint, url_prefix='/questions')

    return app

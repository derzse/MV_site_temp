from flask_sqlalchemy import SQLAlchemy
from utils.seo import LanguageAwareSEOTitleManager

# Initialize database
db = SQLAlchemy()

# Initialize Language-aware SEO manager
seo_manager = LanguageAwareSEOTitleManager(strategy='random')

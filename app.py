from flask import Flask, render_template, request, session, redirect, url_for
from flask_babel import Babel, _, get_locale, ngettext
import os

app = Flask(__name__)
# Configure supported languages
app.config['LANGUAGES'] = {
    'en': 'English',
    'ro': 'Română'
}
app.secret_key = 'Construim viitorul, circuit dupa circuit.'

# Configure Babel
babel = Babel()

def create_app():
    # Babel configuration
    app.config['BABEL_DEFAULT_LOCALE'] = 'ro'
    app.config['BABEL_DEFAULT_TIMEZONE'] = 'UTC'
    
    babel.init_app(app)
    app.babel = babel  # Make sure babel is attached to app
    babel.locale_selector_function = get_locale
    
    return app

# @babel.localeselector
def get_locale():
    # 1. If language is specified in URL args
    if 'lang' in request.args:
        lang = request.args['lang']
		# Use get() method to safely access config
        languages = app.config.get('LANGUAGES', ['en', 'ro'])
        if lang in languages:
            session['language'] = lang
            return lang
    
    # 2. If language is stored in session
    if 'language' in session:
        if session['language'] in app.config['LANGUAGES']:
            return session['language']
    
    # 3. Try to match browser preferences
    return request.accept_languages.best_match(app.config['LANGUAGES'].keys()) or 'ro'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')
	
@app.route('/set_language/<language>')
def set_language(language=None):
    if language in app.config['LANGUAGES']:
        session['language'] = language
    return redirect(request.referrer or url_for('home'))

@app.context_processor
def inject_conf_vars():
    return {
        'LANGUAGES': app.config['LANGUAGES'],
        'CURRENT_LANGUAGE': session.get('language', get_locale()),
        'get_locale': get_locale
    }

if __name__ == '__main__':
    app.run(debug=True)

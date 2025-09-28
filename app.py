from flask import Flask, render_template, request, session, redirect, url_for
from flask_babel import Babel, _, get_locale, gettext, ngettext
import os
from utils import SEOTitleManager
from flask import jsonify

app = Flask(__name__)

app.secret_key = 'Construim viitorul, circuit dupa circuit.'

# Language configuration
app.config['LANGUAGES'] = {
    'ro': 'Română',
    'en': 'English'
}
app.config['BABEL_DEFAULT_LOCALE'] = 'ro'
app.config['BABEL_DEFAULT_TIMEZONE'] = 'UTC'
app.config['BABEL_TRANSLATION_DIRECTORIES'] = './translations'

def get_locale():
    
    # 1. If language is specified in URL args (?lang=en)
    if 'lang' in request.args:
        lang = request.args['lang']
        if lang in app.config['LANGUAGES']:
            session['language'] = lang
            return lang
    
    # 2. If language is stored in session (this should work for your case)
    if 'language' in session:
        lang = session['language']
        if lang in app.config['LANGUAGES']:
            return lang
        
    # 3. Fallback to Romanian
    return 'ro'

# Initialize Babel with the locale selector function (Flask-Babel 4.0.0 style)
babel = Babel(app, locale_selector=get_locale)

# Initialize SEO manager 
seo_manager = SEOTitleManager(strategy='random')

@app.route('/')
def home():
    """Home page with dynamic SEO title"""
    dynamic_title = seo_manager.get_title()
    return render_template('index.html', page_title=dynamic_title)

@app.template_global()
def get_seo_title():
    return seo_manager.get_title()

# Optional: View SEO stats
@app.route('/admin/seo-stats')
def seo_stats():
    """Admin endpoint to monitor title performance"""
    return jsonify({
        'strategy': seo_manager.strategy,
        'title_usage': seo_manager.get_performance_stats(),
        'total_requests': seo_manager.get_total_requests(),
        'available_titles': len(seo_manager.titles)
    })
    
# Optional: Admin endpoint to change strategy
@app.route('/admin/seo-strategy/<strategy>')
def change_seo_strategy(strategy):
    """Admin endpoint to change SEO strategy"""
    try:
        seo_manager.set_strategy(strategy)
        return jsonify({'success': True, 'new_strategy': strategy})
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

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
        '_': gettext,  # Add this line - makes _() available in templates
        'ngettext': ngettext  # For plural translations
    }

@app.route('/debug_translations')
def debug_translations():
    from flask_babel import _
    
    # Get current locale
    current_locale = get_locale()
    
    # Test some translations
    test_translations = {
        'Home Page': _('Home Page'),
        'Stay tuned for updates.': _('Stay tuned for updates.'),
        'donate_message': _('donate_message')
    }
    
    debug_info = f"""
    <h2>Translation Debug</h2>
    <p><strong>Current Locale:</strong> {current_locale}</p>
    <p><strong>Session Language:</strong> {session.get('language', 'not set')}</p>
    <p><strong>Available Languages:</strong> {app.config['LANGUAGES']}</p>
    
    <h3>Translation Tests:</h3>
    <ul>
    """
    
    for key, translation in test_translations.items():
        debug_info += f"<li><strong>{key}:</strong> {translation}</li>"
    
    debug_info += "</ul>"
    
    return debug_info

# Add this test route to your app.py temporarily
@app.route('/test_babel')
def test_babel():
    from flask_babel import _, get_locale
    import os
    
    # Get current locale
    current_locale = get_locale()
    
    # Test direct translation
    try:
        translated = _('Stay tuned for updates.')
    except Exception as e:
        translated = f"ERROR: {e}"
    
    # Check if translation files exist
    ro_mo_exists = os.path.exists('translations/ro/LC_MESSAGES/messages.mo')
    en_mo_exists = os.path.exists('translations/en/LC_MESSAGES/messages.mo')
    
    # Check file sizes
    ro_size = os.path.getsize('translations/ro/LC_MESSAGES/messages.mo') if ro_mo_exists else 0
    en_size = os.path.getsize('translations/en/LC_MESSAGES/messages.mo') if en_mo_exists else 0
    
    return f"""
    <h2>Flask-Babel Test</h2>
    <p><strong>Current Locale:</strong> {current_locale}</p>
    <p><strong>Session Language:</strong> {session.get('language', 'not set')}</p>
    <p><strong>Translation of 'Stay tuned for updates.':</strong> {translated}</p>
    <p><strong>Romanian .mo exists:</strong> {ro_mo_exists} (size: {ro_size} bytes)</p>
    <p><strong>English .mo exists:</strong> {en_mo_exists} (size: {en_size} bytes)</p>
    <p><strong>Translation directory:</strong> {os.path.abspath('translations')}</p>
    """

if __name__ == '__main__':
    app.run(debug=True)

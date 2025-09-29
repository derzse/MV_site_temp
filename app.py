from flask import Flask, render_template, request, session, redirect, url_for
from flask_babel import Babel, _, get_locale, gettext, ngettext
import os
from utils import SEOTitleManager, get_seo_title, get_seo_description
from utils.seo import LanguageAwareSEOTitleManager
from flask import jsonify
from datetime import datetime

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
    
    # 2. If language is stored in session
    if 'language' in session:
        lang = session['language']
        if lang in app.config['LANGUAGES']:
            return lang
        
    # 3. Fallback to Romanian
    return 'ro'

# Initialize Babel with the locale selector function (Flask-Babel 4.0.0 style)
babel = Babel(app, locale_selector=get_locale)

# # Initialize SEO manager 
# seo_manager = SEOTitleManager(strategy='random')

# Initialize Language-aware SEO manager 
seo_manager = LanguageAwareSEOTitleManager(strategy='random')

@app.route('/')
def home():
    """Home page with dynamic SEO title"""
    return render_template('index.html', 
                         page_title=None,  # Will use SEO rotation system
                         page_key='home')

@app.route('/about')
def about():
    return render_template('about.html',
                         page_title=None,
                         page_key='about')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html',
                         page_title=None,
                         page_key='privacy')

@app.route('/set_language/<language>')
def set_language(language=None):
    if language in app.config['LANGUAGES']:
        session['language'] = language
        # Update SEO manager language when user switches
        seo_manager.set_language(language)
    return redirect(request.referrer or url_for('home'))

@app.context_processor
def inject_conf_vars():
    """Make variables available in all templates"""
    
    # Ensure SEO manager matches current language
    current_lang = session.get('language', get_locale())
    seo_manager.set_language(current_lang)
    
    # Create wrapper functions that pass the seo_manager to the utils functions
    def template_get_seo_title(page_key='home', custom_title=None, use_seo_rotation=True):
        print(f"🔧 template_get_seo_title called with: page_key={page_key}, use_seo_rotation={use_seo_rotation}, language={current_lang}")
        try:
            result = get_seo_title(page_key, custom_title, use_seo_rotation, seo_manager)
            print(f"📝 template_get_seo_title result: {result}")
            return result
        except Exception as e:
            print(f"❌ Error in template_get_seo_title: {e}")
            # Fallback to basic translation
            return _('Modus Vivendi Oradea - FTC Robotics Team')
    
    def template_get_seo_description(page_key='home', custom_description=None):
        try:
            return get_seo_description(page_key, custom_description)
        except Exception as e:
            print(f"❌ Error in template_get_seo_description: {e}")
            return _('seo_description_default')
    
    return {
        'LANGUAGES': app.config['LANGUAGES'],
        'CURRENT_LANGUAGE': current_lang,
        'session': session,
        'get_seo_title': template_get_seo_title,
        'get_seo_description': template_get_seo_description,
        'seo_manager': seo_manager,
        '_': gettext,
        'ngettext': ngettext
    }

# ============================================
# ADMIN & DEBUG ROUTES
# ============================================

@app.route('/admin/seo-stats')
def seo_stats():
    """Admin endpoint to monitor title performance"""
    return jsonify({
        'strategy': seo_manager.strategy,
        'current_language': seo_manager.current_language,
        'title_usage': seo_manager.get_performance_stats(),
        'total_requests': seo_manager.get_total_requests(),
        'available_titles': len(seo_manager.titles)
    })
    
@app.route('/admin/seo-strategy/<strategy>')
def change_seo_strategy(strategy):
    """Admin endpoint to change SEO strategy"""
    try:
        seo_manager.set_strategy(strategy)
        return jsonify({'success': True, 'new_strategy': strategy})
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/debug_translations')
def debug_translations():
    
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

@app.route('/debug_seo_calls')
def debug_seo_calls():
    from utils import get_seo_title, get_seo_description
    
    print("=== DEBUG SEO CALLS ===")
    
    # Get current language
    current_lang = session.get('language', get_locale())
    seo_manager.set_language(current_lang)
    
    # Test 1: Direct function call
    try:
        direct_title = get_seo_title('home', use_seo_rotation=True, seo_manager=seo_manager)
        print(f"Direct call result: {direct_title}")
    except Exception as e:
        print(f"Direct call error: {e}")
        direct_title = f"ERROR: {e}"
    
    # Test 2: SEO Manager direct call
    try:
        seo_raw = seo_manager.get_title()
        print(f"SEO Manager raw title: {seo_raw}")
    except Exception as e:
        print(f"SEO Manager error: {e}")
        seo_raw = f"ERROR: {e}"
    
    # Test 3: SEO Manager with specific language
    try:
        seo_en = seo_manager.get_title('en')
        seo_ro = seo_manager.get_title('ro')
        print(f"SEO Manager EN: {seo_en}")
        print(f"SEO Manager RO: {seo_ro}")
    except Exception as e:
        print(f"Language-specific error: {e}")
        seo_en = seo_ro = f"ERROR: {e}"
    
    return f"""
    <h2>SEO Debug Results</h2>
    <p><strong>1. Direct function call:</strong> {direct_title}</p>
    <p><strong>2. SEO Manager (current lang):</strong> {seo_raw}</p>
    <p><strong>3. SEO Manager EN:</strong> {seo_en}</p>
    <p><strong>4. SEO Manager RO:</strong> {seo_ro}</p>
    <hr>
    <p><strong>Current language:</strong> {current_lang}</p>
    <p><strong>SEO Manager language:</strong> {seo_manager.current_language}</p>
    <p><strong>SEO Strategy:</strong> {seo_manager.strategy}</p>
    <hr>
    <a href="/">Back to Home</a> | 
    <a href="/set_language/ro">Switch to RO</a> | 
    <a href="/set_language/en">Switch to EN</a>
    """

# Add this test route to your app.py temporarily
@app.route('/test_babel')
def test_babel():
    
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
	
# Debug route to test SEO rotation + translations
@app.route('/seo_debug')
def seo_debug():
    current = session.get('language', 'ro')
    seo_manager.set_language(current)
    
    # Test multiple title generations to see rotation
    titles = []
    for i in range(5):
        title = get_seo_title('home', use_seo_rotation=True, seo_manager=seo_manager)
        titles.append(title)
    
    # Get SEO manager stats
    stats = seo_manager.get_performance_stats()
    total_requests = seo_manager.get_total_requests()
    
    return f"""
    <h2>🔧 SEO + Translation Debug</h2>
    <p><strong>Current Language:</strong> {current}</p>
    <p><strong>SEO Manager Language:</strong> {seo_manager.current_language}</p>
    <p><strong>SEO Strategy:</strong> {seo_manager.strategy}</p>
    <p><strong>Total Requests:</strong> {total_requests}</p>
    <hr>
    <h3>🎯 Generated Titles (5 calls):</h3>
    <ol>
    {''.join([f'<li>{title}</li>' for title in titles])}
    </ol>
    <hr>
    <h3>📊 Usage Statistics:</h3>
    <ul>
    {''.join([f'<li>{title}: {count} times</li>' for title, count in stats.items()])}
    </ul>
    <hr>
    <h3>🌍 Other Page Titles:</h3>
    <ul>
        <li><strong>About:</strong> {get_seo_title('about', seo_manager=seo_manager)}</li>
        <li><strong>Team:</strong> {get_seo_title('team', seo_manager=seo_manager)}</li>
        <li><strong>Projects:</strong> {get_seo_title('projects', seo_manager=seo_manager)}</li>
    </ul>
    <hr>
    <p>
        <a href="/set_language/ro">🇷🇴 Română</a> | 
        <a href="/set_language/en">🇬🇧 English</a> | 
        <a href="/">🏠 Home</a>
    </p>
    """

@app.context_processor
def inject_current_year():
    return {'current_year': datetime.now().year}

if __name__ == '__main__':
    app.run(debug=True)

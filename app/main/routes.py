from . import main
from flask import render_template, redirect, url_for, jsonify, request, session, current_app, g
from flask_babel import gettext, ngettext
from utils.seo import get_seo_title, get_seo_description
from utils.locale import get_locale
from ..extensions import seo_manager
from datetime import datetime
import os
from flask_babel import _

@main.before_request
def setup_request():
    """Initialize request-specific data"""
    # Set language in g for easy access in templates
    g.language = session.get('language', get_locale())
    # Ensure SEO manager uses the correct language
    seo_manager.set_language(g.language)

@main.route('/')
def home():
    """
    Home page with dynamic SEO title
    
    Returns:
        Rendered home page template with page title and key.
    """
    # Render the home page with dynamic SEO title
    return render_template('index.html', 
                         page_title=None,
                         page_key='home')
    
@main.route('/about')
def about():
    """
    About page with dynamic SEO title

    Returns:
        Rendered about page template with page title and key.
    """
    # Render the about page with dynamic SEO title
    return render_template('about.html',
                         page_title=None,
                         page_key='about')

@main.route('/privacy')
def privacy():
    """
    Privacy policy page with dynamic SEO title
    
    Returns:
        Rendered privacy policy page template with page title and key.
    """
    # Render the privacy policy page with dynamic SEO title
    return render_template('privacy.html',
                         page_title=None,
                         page_key='privacy')

@main.context_processor
def inject_conf_vars():
    """
    Make variables available in all templates for SEO and localization.
    1. Inject configuration variables like supported languages and current language.
    2. Provide utility functions for generating SEO titles and descriptions.
    3. Include translation functions for easy access in templates.
    """

    current_lang = session.get('language', get_locale())
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
    
    def wrapped_get_seo_title(*args, **kwargs):
        return get_seo_title(*args, **kwargs, seo_manager=seo_manager)
    
    # Inject variables and functions into the template context
    from flask_babel import get_locale as babel_get_locale
    return {
        'LANGUAGES': current_app.config['LANGUAGES'],
        'CURRENT_LANGUAGE': g.get('language', 'ro'),
        'session': session,
        'get_seo_title': wrapped_get_seo_title,
        'get_seo_description':  get_seo_description,
        'seo_manager': seo_manager,
        '_': gettext,
        'ngettext': ngettext,
        'babel_locale': str(babel_get_locale())  # Debug line
    }
    
@main.route('/set-language/<language>')
def set_language(language):
    """Change language and redirect back"""
    # print(f"🔧 set_language called with: {language}")
    # print(f"📋 Available languages: {current_app.config['LANGUAGES']}")
    # print(f"✅ Language in config? {language in current_app.config['LANGUAGES']}")
    
    if language in current_app.config['LANGUAGES']:
        session['language'] = language
        session.permanent = True
        # print(f"💾 Session set to: {session.get('language')}")
    # else:
        # print(f"⚠️ Language {language} not in config!")
    return redirect(request.referrer or url_for('main.home'))

# ============================================
# ADMIN & DEBUG ROUTES
# ============================================

@main.route('/admin/seo-stats')
def seo_stats():
    """Admin endpoint to monitor title performance"""
    return jsonify({
        'strategy': seo_manager.strategy,
        'current_language': seo_manager.current_language,
        'title_usage': seo_manager.get_performance_stats(),
        'total_requests': seo_manager.get_total_requests(),
        'available_titles': len(seo_manager.titles)
    })
    
@main.route('/admin/seo-strategy/<strategy>')
def change_seo_strategy(strategy):
    """Admin endpoint to change SEO strategy"""
    try:
        seo_manager.set_strategy(strategy)
        return jsonify({'success': True, 'new_strategy': strategy})
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@main.route('/debug_translations')
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
    <p><strong>Available Languages:</strong> { current_app.config['LANGUAGES']}</p>
    
    <h3>Translation Tests:</h3>
    <ul>
    """
    
    for key, translation in test_translations.items():
        debug_info += f"<li><strong>{key}:</strong> {translation}</li>"
    
    debug_info += "</ul>"
    
    return debug_info

@main.route('/debug_seo_calls')
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
@main.route('/test_babel')
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
@main.route('/seo_debug')
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

@main.context_processor
def inject_current_year():
    return {'current_year': datetime.now().year}

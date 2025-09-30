# utils/locale.py
"""
Internationalization and localization utilities
"""
from flask import request, session
from flask_babel import Babel
from config import Config

# Supported languages
LANGUAGES = Config.LANGUAGES

def get_locale():
    """
    Determine the best locale for the user
    Priority: URL parameter > session > browser preference > default
    """
    
    print(f"🔍 utils.locale.get_locale() called by BABEL")
    print(f"  Session contents: {dict(session)}")
    
    # 1. Check URL parameter
    locale = request.args.get('lang')
    if locale in LANGUAGES:
        session['language'] = locale
        return locale
    
    # 2. Check session
    session_lang = session.get('language')
    # print(f"  Session language: {session_lang}")
    if session_lang and session_lang in LANGUAGES:
        # print(f"  ✅ Returning from session: {session_lang}")
        return session_lang
    # if 'language' in session and session['language'] in LANGUAGES:
    #     return session['language']
    
    # 3. Check browser preferences
    browser_lang = request.accept_languages.best_match(LANGUAGES.keys())
    # print(f"  ⚠️ Falling back to browser: {browser_lang}")
    return browser_lang or 'ro'
    # return request.accept_languages.best_match(LANGUAGES.keys())

def get_supported_languages():
    """Return dictionary of supported languages"""
    return LANGUAGES

def set_language(lang_code):
    """Set language in session"""
    if lang_code in LANGUAGES:
        session['language'] = lang_code
        return True
    return False

def get_current_language():
    """Get current language code"""
    return session.get('language', get_locale())

def get_language_name(lang_code):
    """Get language name from code"""
    return LANGUAGES.get(lang_code, 'Unknown')
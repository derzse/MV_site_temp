#!/usr/bin/env python3
"""
Quick setup script for adding i18n to modusvivendioradea.com
Save this as quick_setup.py in your project root
"""

import os
import sys
import shutil

def create_babel_config():
    """Create babel.cfg file"""
    babel_config = """[python: **.py]
[jinja2: **/templates/**.html]
"""
    with open('babel.cfg', 'w', encoding='utf-8') as f:
        f.write(babel_config)
    print("✅ Created babel.cfg")

def create_translation_directories():
    """Create translation directory structure"""
    dirs = [
        'translations',
        'translations/ro',
        'translations/ro/LC_MESSAGES',
        'translations/en', 
        'translations/en/LC_MESSAGES'
    ]
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
    print("✅ Created translation directories")

def backup_existing_files():
    """Backup existing files before modification"""
    backups = []
    
    if os.path.exists('app.py'):
        shutil.copy2('app.py', 'app_backup.py')
        backups.append('app.py → app_backup.py')
    
    if os.path.exists('templates/base.html'):
        shutil.copy2('templates/base.html', 'templates/base_backup.html')
        backups.append('templates/base.html → templates/base_backup.html')
    
    if backups:
        print("✅ Backed up existing files:")
        for backup in backups:
            print(f"   {backup}")

def create_manage_translations():
    """Create translation management script"""
    script_content = '''#!/usr/bin/env python3
import os
import sys

def extract_messages():
    """Extract all messages for translation"""
    print("🔍 Extracting messages...")
    result = os.system('pybabel extract -F babel.cfg -k _ -o messages.pot .')
    if result == 0:
        print("✅ Messages extracted to messages.pot")
    else:
        print("❌ Failed to extract messages")

def init_language(lang):
    """Initialize a new language"""
    print(f"🌍 Initializing {lang} translations...")
    result = os.system(f'pybabel init -i messages.pot -d translations -l {lang}')
    if result == 0:
        print(f"✅ Initialized {lang} translations")
    else:
        print(f"❌ Failed to initialize {lang} translations")

def update_translations():
    """Update all existing translations"""
    print("🔄 Updating translations...")
    result = os.system('pybabel update -i messages.pot -d translations')
    if result == 0:
        print("✅ Updated all translations")
    else:
        print("❌ Failed to update translations")

def compile_translations():
    """Compile all translations"""
    print("⚙️  Compiling translations...")
    result = os.system('pybabel compile -d translations')
    if result == 0:
        print("✅ Compiled all translations")
    else:
        print("❌ Failed to compile translations")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('🛠️  Translation Management Tool')
        print('Usage:')
        print('  python manage_translations.py extract')
        print('  python manage_translations.py init <language_code>')
        print('  python manage_translations.py update')
        print('  python manage_translations.py compile')
        print('  python manage_translations.py setup    # Run initial setup')
        sys.exit(1)
    
    if sys.argv[1] == 'extract':
        extract_messages()
    elif sys.argv[1] == 'init' and len(sys.argv) == 3:
        init_language(sys.argv[2])
    elif sys.argv[1] == 'update':
        update_translations()
    elif sys.argv[1] == 'compile':
        compile_translations()
    elif sys.argv[1] == 'setup':
        print("🚀 Setting up translations...")
        extract_messages()
        init_language('ro')
        init_language('en')
        print("\\n✅ Translation setup complete!")
        print("\\nNext steps:")
        print("1. Edit translations/ro/LC_MESSAGES/messages.po")
        print("2. Edit translations/en/LC_MESSAGES/messages.po") 
        print("3. Run: python manage_translations.py compile")
'''
    
    with open('manage_translations.py', 'w', encoding='utf-8') as f:
        f.write(script_content)
    print("✅ Created manage_translations.py")

def main():
    print("🚀 Setting up i18n for modusvivendioradea.com")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('templates') or not os.path.exists('static'):
        print("❌ Error: templates/ or static/ directory not found!")
        print("Make sure you're in your modusvivendioradea.com project root directory")
        sys.exit(1)
    
    # Check if Flask-Babel is available
    try:
        import flask_babel
        print("✅ Flask-Babel is installed")
    except ImportError:
        print("❌ Flask-Babel not found. Please install it first:")
        print("  pip install Flask-Babel==3.1.0")
        sys.exit(1)
    
    # Run setup steps
    backup_existing_files()
    create_babel_config()
    create_translation_directories() 
    create_manage_translations()
    
    print("\\n🎉 Initial setup complete!")
    print("\\nNext steps:")
    print("1. Update your app.py file")
    print("2. Update your templates")
    print("3. Run translation setup")
    print("\\nReady for the next step!")

if __name__ == '__main__':
    main()
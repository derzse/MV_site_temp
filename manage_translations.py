#!/usr/bin/env python3
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
        print("\n✅ Translation setup complete!")
        print("\nNext steps:")
        print("1. Edit translations/ro/LC_MESSAGES/messages.po")
        print("2. Edit translations/en/LC_MESSAGES/messages.po") 
        print("3. Run: python manage_translations.py compile")

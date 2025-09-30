"""
Utility modules for the Modus Vivendi website
"""

from .seo import (
    SEOTitleManager,
    LanguageAwareSEOTitleManager,
    create_seo_manager,
    get_seo_title,
    get_seo_description
)
from .locale import (
    get_locale,
    get_supported_languages,
    set_language,
    get_current_language,
    get_language_name,
    LANGUAGES
)

__all__ = [
    'SEOTitleManager',
    'LanguageAwareSEOTitleManager',
    'create_seo_manager',
    'get_seo_title',
    'get_seo_description',
    'create_language_aware_seo_manager',
    'get_locale',
    'get_supported_languages',
    'set_language',
    'get_current_language',
    'get_language_name',
    'LANGUAGES'
]
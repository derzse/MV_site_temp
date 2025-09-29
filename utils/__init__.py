
"""
Utility modules for the Modus Vivendi website
"""

from .seo import SEOTitleManager, create_seo_manager, get_seo_title, get_seo_description

__all__ = ['SEOTitleManager', 'LanguageAwareSEOTitleManager', 'create_seo_manager', 'get_seo_title', 'get_seo_description', 'create_language_aware_seo_manager']
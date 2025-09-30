# ============================================
# File: utils/seo.py
# ============================================

import hashlib
import random
from datetime import datetime
from typing import List, Dict, Optional
from flask import request, current_app
from flask_babel import gettext as _

# Constants
BRAND_NAME = "Modus Vivendi Oradea"

class SEOTitleManager:
    """
    Manages dynamic SEO titles with various rotation strategies
    """
    
    # Default SEO title variations - can be overridden
    DEFAULT_TITLES = [
        "Modus Vivendi Oradea - Prima echipă FTC din Oradea | Robotică de excelență",
        "Echipa FTC Modus Vivendi | 8 ani de experiență în robotică competițională",
        "Robotică FTC Oradea - Modus Vivendi | FIRST Tech Challenge România",
        "Modus Vivendi - Echipa de robotică din Oradea | FTC Champions",
        "FIRST Tech Challenge Oradea | Modus Vivendi - Inovație în robotică",
        "Robotică competițională Oradea | Modus Vivendi FTC Team",
        "Modus Vivendi - Design Award Winners | Prima echipă FTC Oradea",
        "STEM Education Oradea | Echipa FTC Modus Vivendi",
        "Robotică pentru tineri Oradea | Modus Vivendi FIRST Tech Challenge"
    ]
    
    def __init__(self, titles: Optional[List[str]] = None, strategy: str = 'consistent'):
        """
        Initialize SEO Title Manager
        
        Args:
            titles: List of title variations (uses DEFAULT_TITLES if None)
            strategy: Rotation strategy ('random', 'consistent', 'daily', 'weekly', 'hourly')
        """
        self.titles = titles or self.DEFAULT_TITLES
        self.strategy = strategy
        self.performance_stats = {}
        
    def get_title(self) -> str:
        """Get a title based on the configured strategy"""
        strategy_methods = {
            'random': self._get_random_title,
            'consistent': self._get_consistent_title,
            'daily': lambda: self._get_time_based_title('daily'),
            'weekly': lambda: self._get_time_based_title('weekly'),
            'hourly': lambda: self._get_time_based_title('hourly')
        }
        
        method = strategy_methods.get(self.strategy, lambda: self.titles[0])
        title = method()
        
        # Track usage
        self._track_usage(title)
        return title
        
    def _get_random_title(self) -> str:
        """Random title selection"""
        return random.choice(self.titles)
        
    def _get_consistent_title(self) -> str:
        """
        Consistent title per visitor (based on IP + User Agent)
        Same visitor always gets the same title
        """
        try:
            # Create a unique identifier for the visitor
            visitor_identifier = self._get_visitor_identifier()
            
            # Convert to index
            title_index = int(visitor_identifier[:8], 16) % len(self.titles)
            return self.titles[title_index]
            
        except Exception as e:
            if current_app:
                current_app.logger.warning(f"Error in consistent title generation: {e}")
            return self.titles[0]  # Fallback
            
    def _get_time_based_title(self, period: str) -> str:
        """Time-based title rotation"""
        now = datetime.now()
        
        time_units = {
            'hourly': now.hour,
            'daily': now.timetuple().tm_yday,  # Day of year
            'weekly': now.isocalendar()[1]     # Week number
        }
        
        time_unit = time_units.get(period, 0)
        title_index = time_unit % len(self.titles)
        return self.titles[title_index]
        
    def _get_visitor_identifier(self) -> str:
        """
        Create a unique identifier for the visitor
        """
        # Combine IP address and User Agent for uniqueness
        ip_address = request.remote_addr or 'unknown'
        user_agent = request.headers.get('User-Agent', 'unknown')
        
        # Create hash
        visitor_string = f"{ip_address}:{user_agent}"
        return hashlib.md5(visitor_string.encode()).hexdigest()
        
    def _track_usage(self, title: str) -> None:
        """
        Track how often each title is used
        """
        self.performance_stats[title] = self.performance_stats.get(title, 0) + 1
        
    def get_performance_stats(self) -> Dict[str, int]:
        """
        Get usage statistics for all titles
        """
        return self.performance_stats.copy()
        
    def get_total_requests(self) -> int:
        """
        Get total number of title requests served
        """
        return sum(self.performance_stats.values())
        
    def reset_stats(self) -> None:
        """
        Reset performance statistics
        """
        self.performance_stats.clear()
        
    def add_title(self, title: str) -> None:
        """
        Add a new title variation
        """
        if title not in self.titles:
            self.titles.append(title)
            
    def remove_title(self, title: str) -> bool:
        """
        Remove a title variation
        Returns True if removed, False if not found
        """
        try:
            self.titles.remove(title)
            return True
        except ValueError:
            return False
            
    def set_strategy(self, strategy: str) -> None:
        """
        Change the rotation strategy
        """
        valid_strategies = ['random', 'consistent', 'daily', 'weekly', 'hourly']
        if strategy not in valid_strategies:
            raise ValueError(f"Invalid strategy. Must be one of: {valid_strategies}")
        self.strategy = strategy
        
# Add this to your utils/seo.py

class LanguageAwareSEOTitleManager(SEOTitleManager):
    """
    SEO Title Manager with language-specific title sets
    """
    
    def __init__(self, strategy: str = 'consistent'):
        # Romanian titles
        self.titles_ro = [
            "Modus Vivendi Oradea - Prima echipă FTC din Oradea | Robotică de excelență",
            "Echipa FTC Modus Vivendi | 8 ani de experiență în robotică competițională",
            "Robotică FTC Oradea - Modus Vivendi | FIRST Tech Challenge România",
            "Modus Vivendi - Echipa de robotică din Oradea | FTC Champions",
            "FIRST Tech Challenge Oradea | Modus Vivendi - Inovație în robotică",
            "Robotică competițională Oradea | Modus Vivendi FTC Team",
            "Modus Vivendi - Design Award Winners | Prima echipă FTC Oradea",
            "STEM Education Oradea | Echipa FTC Modus Vivendi",
            "Robotică pentru tineri Oradea | Modus Vivendi FIRST Tech Challenge"
        ]
        
        # English titles
        self.titles_en = [
            "Modus Vivendi Oradea - First FTC Team from Oradea | Robotics Excellence",
            "FTC Team Modus Vivendi | 8 Years of Competitive Robotics Experience",
            "FTC Robotics Oradea - Modus Vivendi | FIRST Tech Challenge Romania",
            "Modus Vivendi - Oradea Robotics Team | FTC Champions",
            "FIRST Tech Challenge Oradea | Modus Vivendi - Innovation in Robotics",
            "Competitive Robotics Oradea | Modus Vivendi FTC Team",
            "Modus Vivendi - Design Award Winners | First FTC Team Oradea",
            "STEM Education Oradea | FTC Team Modus Vivendi",
            "Robotics for Youth Oradea | Modus Vivendi FIRST Tech Challenge"
        ]
        
        # Initialize with Romanian titles (default)
        super().__init__(titles=self.titles_ro, strategy=strategy)
        self.current_language = 'ro'
        
    def set_language(self, language: str):
        """Switch between Romanian and English title sets"""
        if language == 'ro':
            self.titles = self.titles_ro
            self.current_language = 'ro'
        elif language == 'en':
            self.titles = self.titles_en
            self.current_language = 'en'
        else:
            # Default to Romanian
            self.titles = self.titles_ro
        
        self.current_language = language
        
    def get_title(self, language: str = None) -> str:
        """Get title with optional language override"""
        if language and language != self.current_language:
            # Temporarily switch language
            old_titles = self.titles
            old_language = self.current_language
            
            self.set_language(language)
            title = super().get_title()
            
            # Restore previous state
            self.titles = old_titles
            self.current_language = old_language
            
            return title
        else:
            return super().get_title()

# Factory function for easy instantiation
def create_seo_manager(strategy: str = 'consistent') -> SEOTitleManager:
    """
    Factory function to create SEOTitleManager with default settings
    """
    return SEOTitleManager(strategy=strategy)


# ============================================
# SEO TITLE & DESCRIPTION FUNCTIONS
# ============================================

def get_seo_title(page_key='home', custom_title=None, use_seo_rotation=True, seo_manager=None):
    """
    Generate SEO-optimized translated titles
    Args:
        page_key: The page identifier for translation lookup
        custom_title: Optional custom title override
        use_seo_rotation: Whether to use your SEO rotation system
        seo_manager: Instance of SEOTitleManager (optional)
    """
    if custom_title:
        return f"{_(custom_title)} - {BRAND_NAME}"
    
    # Use your sophisticated SEO rotation for home page
    if page_key == 'home' and use_seo_rotation and seo_manager:
        # Get the SEO-optimized title using your rotation strategy
        base_title = seo_manager.get_title()

        # Translate the title - this will be handled by your translation keys
        return f"{_(base_title)}"

    # Define page-specific SEO titles with translation keys for other pages
    seo_titles = {
        'home': _('Modus Vivendi Oradea - FTC Robotics Team | Innovation in Oradea'),
        'about': _('About Modus Vivendi | FTC Team Oradea - 8 Years Experience'),
        'privacy': _('Privacy Policy | Modus Vivendi Oradea FTC Team'),
        'contact': _('Contact Modus Vivendi | FTC Robotics Team Oradea'),
        'projects': _('Our FTC Projects | Modus Vivendi Robotics Oradea'),
        'events': _('FTC Events & Competitions | Modus Vivendi Oradea'),
        'team': _('Our FTC Team Members | Modus Vivendi Oradea'),
        'achievements': _('FTC Awards & Achievements | Modus Vivendi Oradea'),
    }
    
    return seo_titles.get(page_key, _('Modus Vivendi Oradea - FIRST Tech Challenge Team'))


def get_seo_description(page_key='home', custom_description=None):
    """Generate SEO-optimized translated meta descriptions"""
    if custom_description:
        return _(custom_description)
    
    seo_descriptions = {
        'home': _('seo_description_home'),
        'about': _('seo_description_about'), 
        'privacy': _('seo_description_privacy'),
        'contact': _('seo_description_contact'),
        'team': _('seo_description_team'),
        'projects': _('seo_description_projects'),
        'achievements': _('seo_description_achievements'),
    }
    
    return seo_descriptions.get(page_key, _('seo_description_default'))


# # ============================================
# # FACTORY FUNCTIONS
# # ============================================

# def create_seo_manager(strategy: str = 'consistent') -> SEOTitleManager:
#     """Factory function to create SEOTitleManager"""
#     return SEOTitleManager(strategy=strategy)


# def create_language_aware_seo_manager(strategy: str = 'consistent') -> LanguageAwareSEOTitleManager:
#     """Factory function to create LanguageAwareSEOTitleManager"""
#     return LanguageAwareSEOTitleManager(strategy=strategy)
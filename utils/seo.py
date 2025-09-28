# ============================================
# File: utils/seo.py
# ============================================

import hashlib
import random
from datetime import datetime
from typing import List, Dict, Optional
from flask import request, current_app


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
        """
        Get a title based on the configured strategy
        """
        if self.strategy == 'random':
            title = self._get_random_title()
        elif self.strategy == 'consistent':
            title = self._get_consistent_title()
        elif self.strategy == 'daily':
            title = self._get_time_based_title('daily')
        elif self.strategy == 'weekly':
            title = self._get_time_based_title('weekly')
        elif self.strategy == 'hourly':
            title = self._get_time_based_title('hourly')
        else:
            # Default to first title if strategy is unknown
            title = self.titles[0]
            
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
            current_app.logger.warning(f"Error in consistent title generation: {e}")
            return self.titles[0]  # Fallback to first title
            
    def _get_time_based_title(self, period: str) -> str:
        """
        Time-based title rotation
        """
        now = datetime.now()
        
        if period == 'hourly':
            time_unit = now.hour
        elif period == 'daily':
            time_unit = now.timetuple().tm_yday  # Day of year
        elif period == 'weekly':
            time_unit = now.isocalendar()[1]  # Week number
        else:
            time_unit = 0
            
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
        if title not in self.performance_stats:
            self.performance_stats[title] = 0
        self.performance_stats[title] += 1
        
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
        if strategy in valid_strategies:
            self.strategy = strategy
        else:
            raise ValueError(f"Invalid strategy. Must be one of: {valid_strategies}")


# Factory function for easy instantiation
def create_seo_manager(strategy: str = 'consistent') -> SEOTitleManager:
    """
    Factory function to create SEOTitleManager with default settings
    """
    return SEOTitleManager(strategy=strategy)
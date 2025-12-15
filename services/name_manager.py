"""
Name management system for dynasty generation.

Handles loading and providing names for different cultures. Names are loaded once
per application run and cached in memory.
"""

from typing import Dict, List
import os
import random


class NameProvider:
    """Provides names for a specific culture."""
    
    def __init__(self, male_names: List[str], female_names: List[str]):
        """
        Initialize the provider with lists of male and female names.
        
        Args:
            male_names: List of male given names
            female_names: List of female given names
        """
        self.male_names = male_names
        self.female_names = female_names
    
    def get_random_male_name(self, rng: random.Random) -> str:
        """Get a random male name."""
        return rng.choice(self.male_names)
    
    def get_random_female_name(self, rng: random.Random) -> str:
        """Get a random female name."""
        return rng.choice(self.female_names)


class NameManager:
    """
    Singleton-like manager for loading and caching name providers for different cultures.
    
    Ensures names are only loaded once per application run.
    """
    
    _providers: Dict[str, NameProvider] = {}
    
    @classmethod
    def load_culture(cls, culture: str, base_path: str = None) -> NameProvider:
        """
        Load a culture's name provider. Cached after first load.
        
        Args:
            culture: Culture name (e.g., 'chinese', 'english')
            base_path: Path to namelists directory. If None, uses current working directory.
        
        Returns:
            NameProvider for the specified culture
        
        Raises:
            FileNotFoundError: If name files not found for the culture
            ValueError: If name files are empty
        """
        # Return cached provider if already loaded
        if culture in cls._providers:
            return cls._providers[culture]
        
        # Determine file paths
        if base_path is None:
            base_path = os.path.join(os.path.dirname(__file__), '..', 'namelists')
        
        # Map culture to file prefixes
        culture_prefix_map = {
            'chinese': 'han',
            'english': 'english',
            'french': 'french',
            'german': 'german',
        }
        
        prefix = culture_prefix_map.get(culture.lower(), culture.lower())
        male_file = os.path.join(base_path, f"{prefix}_names_male.txt")
        female_file = os.path.join(base_path, f"{prefix}_names_female.txt")
        
        # Load names
        try:
            with open(male_file, 'r', encoding='utf-8') as f:
                male_names = [line.strip() for line in f if line.strip()]
            
            with open(female_file, 'r', encoding='utf-8') as f:
                female_names = [line.strip() for line in f if line.strip()]
        except FileNotFoundError as e:
            raise FileNotFoundError(
                f"Could not find name files for culture '{culture}'. "
                f"Expected: {male_file} and {female_file}"
            ) from e
        
        if not male_names or not female_names:
            raise ValueError(
                f"Name files for culture '{culture}' are empty. "
                f"Male: {len(male_names)}, Female: {len(female_names)}"
            )
        
        # Create and cache provider
        provider = NameProvider(male_names, female_names)
        cls._providers[culture] = provider
        
        return provider
    
    @classmethod
    def get_available_cultures(cls) -> List[str]:
        """Get list of available cultures."""
        return ['chinese', 'english', 'french', 'german']
    
    @classmethod
    def reset(cls):
        """Reset all cached providers. Useful for testing."""
        cls._providers.clear()

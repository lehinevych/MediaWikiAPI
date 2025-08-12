"""
MediaWiki API version handling utilities.

This module provides functionality for detecting and managing MediaWiki API versions,
ensuring compatibility across different MediaWiki installations.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple


@dataclass
class MediaWikiVersion:
    """
    Represents a MediaWiki API version.
    
    Attributes:
        major (int): Major version number
        minor (int): Minor version number
        patch (int): Patch version number
        generator (str): Generator string (e.g., "MediaWiki 1.34.0-wmf.19")
    """
    major: int
    minor: int
    patch: int
    generator: str

    @classmethod
    def from_generator_string(cls, generator: str) -> 'MediaWikiVersion':
        """
        Create a MediaWikiVersion from a generator string.
        
        Args:
            generator: Generator string from the MediaWiki API response
            
        Returns:
            MediaWikiVersion object
            
        Example:
            >>> MediaWikiVersion.from_generator_string("MediaWiki 1.34.0-wmf.19")
            MediaWikiVersion(major=1, minor=34, patch=0, generator="MediaWiki 1.34.0-wmf.19")
        """
        # Remove any suffix after the version numbers
        parts = generator.split()
        if len(parts) < 2:
            # If we can't parse it, assume a minimal supported version
            return cls(1, 19, 0, generator)
            
        version_str = parts[1]
        version_parts = version_str.split('.')
        
        # Parse the version numbers
        major = int(version_parts[0]) if len(version_parts) > 0 else 1
        
        # For minor, remove any suffix after a dash
        minor_str = version_parts[1] if len(version_parts) > 1 else "0"
        if '-' in minor_str:
            minor_str = minor_str.split('-')[0]
        minor = int(minor_str)
        
        # For patch, remove any suffix after a dash
        patch_str = version_parts[2] if len(version_parts) > 2 else "0"
        if '-' in patch_str:
            patch_str = patch_str.split('-')[0]
        patch = int(patch_str)
        
        return cls(major, minor, patch, generator)
        
    def __lt__(self, other: 'MediaWikiVersion') -> bool:
        """Compare if this version is less than another version."""
        if self.major != other.major:
            return self.major < other.major
        if self.minor != other.minor:
            return self.minor < other.minor
        return self.patch < other.patch
        
    def __le__(self, other: 'MediaWikiVersion') -> bool:
        """Compare if this version is less than or equal to another version."""
        return self < other or self == other
    
    def __gt__(self, other: 'MediaWikiVersion') -> bool:
        """Compare if this version is greater than another version."""
        return not (self <= other)
        
    def __ge__(self, other: 'MediaWikiVersion') -> bool:
        """Compare if this version is greater than or equal to another version."""
        return not (self < other)
        
    def __str__(self) -> str:
        """String representation of the version."""
        return f"{self.major}.{self.minor}.{self.patch}"
        

# Define version constants for key MediaWiki versions
MEDIAWIKI_1_19 = MediaWikiVersion(1, 19, 0, "MediaWiki 1.19.0")  # Oldest supported version
MEDIAWIKI_1_25 = MediaWikiVersion(1, 25, 0, "MediaWiki 1.25.0")  # Added some new features
MEDIAWIKI_1_32 = MediaWikiVersion(1, 32, 0, "MediaWiki 1.32.0")  # Added more features
MEDIAWIKI_1_34 = MediaWikiVersion(1, 34, 0, "MediaWiki 1.34.0")  # Enhanced content parsing
MEDIAWIKI_1_35 = MediaWikiVersion(1, 35, 0, "MediaWiki 1.35.0")  # Long-term support release
MEDIAWIKI_1_39 = MediaWikiVersion(1, 39, 0, "MediaWiki 1.39.0")  # Latest long-term support release


# Dictionary mapping MediaWiki versions to available features
FEATURE_AVAILABILITY: Dict[str, MediaWikiVersion] = {
    # Feature: Minimum version required
    "extracts": MEDIAWIKI_1_25,              # TextExtracts extension (summary)
    "pageimages": MEDIAWIKI_1_25,            # PageImages extension (thumbnail)
    "coordinates": MEDIAWIKI_1_25,           # GeoData extension (coordinates)
    "pageprops": MEDIAWIKI_1_25,             # Page properties
    "infobox_extraction": MEDIAWIKI_1_34,    # Enhanced HTML parsing for infoboxes
    "content_html": MEDIAWIKI_1_32,          # Enhanced content HTML parsing
    "section_html": MEDIAWIKI_1_32,          # Enhanced section HTML parsing
    "advanced_references": MEDIAWIKI_1_35,    # Advanced reference extraction
    "structured_data": MEDIAWIKI_1_39        # Structured data support
}


# For server-side caching of version
_version_cache: Dict[str, MediaWikiVersion] = {}


def get_required_version_for_feature(feature: str) -> MediaWikiVersion:
    """
    Get the minimum required MediaWiki version for a specific feature.
    
    Args:
        feature: Feature name
        
    Returns:
        MediaWikiVersion object representing the minimum required version
        
    Raises:
        KeyError: If the feature is unknown
    """
    if feature not in FEATURE_AVAILABILITY:
        raise KeyError(f"Unknown feature: {feature}")
    return FEATURE_AVAILABILITY[feature]


def is_feature_available(feature: str, version: MediaWikiVersion) -> bool:
    """
    Check if a feature is available in the given MediaWiki version.
    
    Args:
        feature: Feature name
        version: MediaWiki version to check against
        
    Returns:
        True if the feature is available, False otherwise
    """
    try:
        required_version = get_required_version_for_feature(feature)
        return version >= required_version
    except KeyError:
        return False


def cache_version(api_url: str, version: MediaWikiVersion) -> None:
    """
    Cache a MediaWiki version for a specific API URL.
    
    Args:
        api_url: The API URL
        version: The detected MediaWiki version
    """
    _version_cache[api_url] = version


def get_cached_version(api_url: str) -> Optional[MediaWikiVersion]:
    """
    Get a cached MediaWiki version for a specific API URL.
    
    Args:
        api_url: The API URL
        
    Returns:
        MediaWikiVersion if cached, None otherwise
    """
    return _version_cache.get(api_url)


def clear_version_cache() -> None:
    """Clear the version cache."""
    _version_cache.clear()


def get_available_features(version: MediaWikiVersion) -> List[str]:
    """
    Get a list of all features available in the given MediaWiki version.
    
    Args:
        version: MediaWiki version to check
        
    Returns:
        List of available feature names
    """
    return [
        feature for feature, required_version in FEATURE_AVAILABILITY.items()
        if version >= required_version
    ]
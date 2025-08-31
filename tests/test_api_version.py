"""
Tests for MediaWiki API version handling.
"""

import pytest
from unittest.mock import MagicMock, patch

from mediawikiapi.common.api_version import (
    MediaWikiVersion,
    is_feature_available,
    get_required_version_for_feature,
    MEDIAWIKI_1_19,
    MEDIAWIKI_1_25,
    MEDIAWIKI_1_34,
    MEDIAWIKI_1_39,
)
from mediawikiapi.config import Config


class TestMediaWikiVersion:
    """Tests for the MediaWikiVersion class"""

    def test_version_parsing(self):
        """Test parsing of version strings"""
        # Standard version format
        version = MediaWikiVersion.from_generator_string("MediaWiki 1.34.0")
        assert version.major == 1
        assert version.minor == 34
        assert version.patch == 0

        # Version with suffix
        version = MediaWikiVersion.from_generator_string("MediaWiki 1.35.0-wmf.20")
        assert version.major == 1
        assert version.minor == 35
        assert version.patch == 0

        # Unusual format
        version = MediaWikiVersion.from_generator_string("MediaWiki 1.40-alpha")
        assert version.major == 1
        assert version.minor == 40
        assert version.patch == 0

        # Minimal format
        version = MediaWikiVersion.from_generator_string("MediaWiki 1")
        assert version.major == 1
        assert version.minor == 0
        assert version.patch == 0

        # Invalid format (should not crash)
        version = MediaWikiVersion.from_generator_string("Unknown")
        assert version.major == 1
        assert version.minor == 19
        assert version.patch == 0

    def test_version_comparison(self):
        """Test version comparisons"""
        v1_34 = MediaWikiVersion(1, 34, 0, "")
        v1_35 = MediaWikiVersion(1, 35, 0, "")
        v1_35_1 = MediaWikiVersion(1, 35, 1, "")
        v2_0 = MediaWikiVersion(2, 0, 0, "")

        # Less than
        assert v1_34 < v1_35
        assert v1_35 < v1_35_1
        assert v1_35_1 < v2_0

        # Greater than
        assert v2_0 > v1_35_1
        assert v1_35_1 > v1_35
        assert v1_35 > v1_34

        # Equal
        assert v1_34 == MediaWikiVersion(1, 34, 0, "")
        assert v1_35 == MediaWikiVersion(1, 35, 0, "")

        # Less than or equal
        assert v1_34 <= v1_34
        assert v1_34 <= v1_35

        # Greater than or equal
        assert v1_35 >= v1_35
        assert v1_35 >= v1_34


class TestFeatureAvailability:
    """Tests for feature availability checking"""

    def test_required_version(self):
        """Test getting required version for features"""
        # Check some key features
        extracts_version = get_required_version_for_feature("extracts")
        assert extracts_version == MEDIAWIKI_1_25

        infobox_version = get_required_version_for_feature("infobox_extraction")
        assert infobox_version == MEDIAWIKI_1_34

        # Unknown feature should raise KeyError
        with pytest.raises(KeyError):
            get_required_version_for_feature("nonexistent_feature")

    def test_feature_availability(self):
        """Test checking if features are available"""
        # Old version
        assert is_feature_available("extracts", MEDIAWIKI_1_25)
        assert not is_feature_available("infobox_extraction", MEDIAWIKI_1_25)

        # Newer version
        assert is_feature_available("extracts", MEDIAWIKI_1_34)
        assert is_feature_available("infobox_extraction", MEDIAWIKI_1_34)

        # Latest version should have all features
        assert is_feature_available("extracts", MEDIAWIKI_1_39)
        assert is_feature_available("infobox_extraction", MEDIAWIKI_1_39)
        assert is_feature_available("structured_data", MEDIAWIKI_1_39)

        # Unknown feature
        assert not is_feature_available("nonexistent_feature", MEDIAWIKI_1_39)


class TestConfigVersionHandling:
    """Tests for version handling in Config"""

    def test_version_storage_and_retrieval(self):
        """Test storing and retrieving versions in Config"""
        config = Config()
        api_url = "https://en.wikipedia.org/w/api.php"
        version = MediaWikiVersion(1, 35, 0, "MediaWiki 1.35.0")

        # Store the version
        config.set_api_version(api_url, version)

        # Retrieve the version
        retrieved = config.get_api_version(api_url)
        assert retrieved == version
        assert retrieved.major == 1
        assert retrieved.minor == 35
        assert retrieved.patch == 0

        # Non-existent URL
        assert config.get_api_version("https://nonexistent.org/api.php") is None

    def test_feature_compatibility_mode(self):
        """Test feature compatibility mode in Config"""
        # With compatibility mode enabled (default)
        config = Config()
        assert config.feature_compatibility_mode is True
        assert config.is_feature_available("any_feature", "any_url") is True

        # With compatibility mode disabled
        config = Config(feature_compatibility_mode=False)
        assert config.feature_compatibility_mode is False

        # Should return False for unknown URL
        assert config.is_feature_available("extracts", "unknown_url") is False

        # Set a version and check again
        api_url = "https://en.wikipedia.org/w/api.php"
        config.set_api_version(api_url, MEDIAWIKI_1_25)
        assert config.is_feature_available("extracts", api_url) is True
        assert config.is_feature_available("infobox_extraction", api_url) is False


if __name__ == "__main__":
    pytest.main()

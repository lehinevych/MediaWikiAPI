# -*- coding: utf-8 -*-
import os
import pytest
import pytest_asyncio
import vcr

# Configure VCR for test recordings
os.environ["VCR_RECORD_MODE"] = "new_episodes"


# Setup VCR for both sync and async tests
@pytest.fixture(scope="module")
def vcr_config():
    return {
        "filter_headers": ["User-Agent"],
        "record_mode": "new_episodes",
        "serializer": "yaml",
        "cassette_library_dir": "tests/cassettes",
    }


# Setup async VCR
@pytest_asyncio.fixture(scope="module")
async def async_vcr(vcr_config):
    """VCR fixture for async tests."""
    with vcr.use_cassette(**vcr_config) as cassette:
        yield cassette

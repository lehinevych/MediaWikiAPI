#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Update test fixtures with current Wikipedia API responses."""

import json
import os
from typing import Dict, Any

from mediawikiapi import MediaWikiAPI

# Initialize API client
api = MediaWikiAPI()


def update_test_data() -> None:
    """Update test data with current Wikipedia API responses."""
    # Create mock_data directory if it doesn't exist
    os.makedirs("tests/mock_data", exist_ok=True)

    # Update search data
    search_data = {
        "barack.search": api.search("Barack Obama"),
        "porsche.search": api.search("Porsche", results=3),
    }

    # Update page data
    celtuce = api.page("Celtuce")
    page_data = {
        "celtuce.summary": celtuce.summary,
        "celtuce.content": celtuce.content,
        "celtuce.images": celtuce.images,
        "celtuce.references": celtuce.references,
        "celtuce.links": celtuce.links,
        "celtuce.sections": celtuce.sections,
        "celtuce.revid": celtuce.revision_id,
        "celtuce.parentid": celtuce.parent_id,
        "celtuce.infobox": celtuce.infobox,
        "celtuce.categories": celtuce.categories,
    }

    # Update geosearch data
    geo_data = {
        "great_wall_of_china.geo_seach_with_radius": api.geosearch(
            40.67693, 117.23193, radius=10000
        ),
    }

    # Combine all data
    mock_data = {**search_data, **page_data, **geo_data}

    # Write updated mock data to file
    with open("tests/mock_data/updated_data.json", "w") as f:
        json.dump(mock_data, f, indent=2, sort_keys=True)

    # Write instructions for updating tests
    with open("tests/mock_data/UPDATE_INSTRUCTIONS.md", "w") as f:
        f.write("""# Test Data Update Instructions

The test data has been updated to match the current Wikipedia API responses.

To update your tests:

1. Review the changes in `tests/mock_data/updated_data.json`
2. Update the mock data in `tests/request_mock_data.py` with the new values
3. Run the tests to verify they pass with the updated data

Note: Wikipedia content changes over time, so tests that compare exact content will need to be updated.
""")

    print("Test data updated successfully!")
    print("Review tests/mock_data/updated_data.json and update tests accordingly.")


if __name__ == "__main__":
    update_test_data()

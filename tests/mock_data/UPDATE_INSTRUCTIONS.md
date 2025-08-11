# Test Data Update Instructions

The test data has been updated to match the current Wikipedia API responses.

To update your tests:

1. Review the changes in `tests/mock_data/updated_data.json`
2. Update the mock data in `tests/request_mock_data.py` with the new values
3. Run the tests to verify they pass with the updated data

Note: Wikipedia content changes over time, so tests that compare exact content will need to be updated.

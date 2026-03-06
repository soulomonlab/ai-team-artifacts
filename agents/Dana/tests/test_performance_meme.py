import os
import pytest

# Performance tests are placeholders; recommend using Locust or k6 in CI.
# This pytest file validates that performance tooling env vars exist and provides
# a basic smoke check.

STAGING_BASE_URL = os.getenv('STAGING_BASE_URL')
PERF_TOOL = os.getenv('PERF_TOOL', 'locust')

@pytest.mark.skipif(not STAGING_BASE_URL, reason="STAGING_BASE_URL not set")
def test_performance_env_check():
    """Ensure performance test tooling and endpoints are configured"""
    assert PERF_TOOL in ('locust', 'k6'), 'PERF_TOOL must be locust or k6 in CI'
    assert os.getenv('PERF_TEST_BUCKET'), 'PERF_TEST_BUCKET must be set for storing artifacts'


if __name__ == '__main__':
    pytest.main([__file__])

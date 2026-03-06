This directory contains QA test artifacts for the Quick-win MVP.

Files:
- test_e2e_auth.py: Pytest E2E test covering signup->login->profile update
- locustfile_auth.py: Locust load test targeting auth endpoints
- qa_test_plan_quickwin_mvp.md: QA test plan and pass criteria

Usage examples:
- Run E2E: BASE_URL=https://staging.example.com pytest output/tests/test_e2e_auth.py -q
- Run Locust: locust -f output/tests/locustfile_auth.py --host=https://staging.example.com

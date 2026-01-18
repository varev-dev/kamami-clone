## Setup

Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running tests

The test suite uses the `BASE_URL` environment variable to specify the target application URL. Defaults to `https://localhost:8443/pl/` if not set.

```bash
BASE_URL="https://your-url.com/" pytest
```

## Email Uniqueness

**Important:** The test uses a hardcoded email address. If running the test multiple times, you must either:

1. Use a unique email for each test run (modify `TEST_EMAIL` constant)
2. Delete the test user from the database between runs
3. Use timestamped emails (e.g., `john.doe+{timestamp}@example.com`)

## Download Directory

Test downloads (invoices) are saved to `./Resources/downloads/` by default, configurable through the `DOWNLOAD_PATH` constant.
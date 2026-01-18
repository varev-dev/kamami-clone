# Tests

## Setup

Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration

The test suite uses the `BASE_URL` environment variable to specify the target application URL. Defaults to `https://localhost:8443/pl/` if not set.

```bash
BASE_URL="https://your-url.com/pl/" pytest
```
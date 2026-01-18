# E2E Tests

End-to-end test suite using Selenium and pytest.

## Project Structure

```
tests/
├── config.py              # Test configuration and constants
├── conftest.py            # Pytest fixtures (WebDriver setup)
├── pages/                 # Page Object Model classes
│   ├── __init__.py
│   ├── base_page.py       # Base page class with common methods
│   ├── home_page.py       # Homepage functionality
│   ├── category_page.py   # Category listing pages
│   ├── product_page.py    # Product detail pages
│   ├── search_page.py     # Search results pages
│   ├── cart_page.py       # Shopping cart page
│   ├── checkout_page.py   # Multi-step checkout process
│   └── confirmation_page.py # Order confirmation page
├── test_ecommerce_flow.py # Main E2E test
├── Resources/
│   └── downloads/         # Downloaded invoice files
└── requirements.txt       # Python dependencies
```

## Setup

Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration

Test configuration is centralized in `config.py`. You can override settings using environment variables:

### Available Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `BASE_URL` | `https://localhost:8443/pl/` | Target application URL |
| `CATEGORY_COUNT` | `2` | Number of categories to test |
| `PRODUCTS_PER_CATEGORY` | `10` | Products to add per category |
| `PRODUCTS_TO_REMOVE` | `3` | Products to remove from cart |
| `SEARCH_QUERY` | `druk` | Search term to test |
| `DELIVERY_OPTION_ID` | `2` | Delivery method selection |
| `PAYMENT_OPTION_ID` | `2` | Payment method selection |
| `TEST_FIRST_NAME` | `John` | Test user first name |
| `TEST_LAST_NAME` | `Doe` | Test user last name |
| `TEST_EMAIL` | `john.doe@example.com` | Test user email |
| `TEST_PASSWORD` | `password` | Test user password |
| `TEST_ADDRESS` | `123 Main St` | Test address |
| `TEST_POSTCODE` | `12-345` | Test postal code |
| `TEST_CITY` | `Anytown` | Test city |
| `IMPLICIT_WAIT` | `10` | Selenium implicit wait (seconds) |
| `EXPLICIT_WAIT` | `10` | Selenium explicit wait (seconds) |
| `WINDOW_WIDTH` | `1920` | Browser window width |
| `WINDOW_HEIGHT` | `1080` | Browser window height |

## Running Tests

### Basic Usage

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test
pytest test_ecommerce_flow.py::test_ecommerce_flow
```

### With Custom Configuration

```bash
# Custom BASE_URL
BASE_URL="https://your-url.com/" pytest

# Multiple environment variables
BASE_URL="https://staging.example.com/" TEST_EMAIL="test@example.com" pytest

# Using a different search query
SEARCH_QUERY="resistor" pytest
```

## Email Uniqueness

**Important:** The test uses a configurable email address. If running the test multiple times, you must either:

1. Set a unique email for each run using `TEST_EMAIL` environment variable
2. Delete the test user from the database between runs
3. Use timestamped emails (e.g., `john.doe+{timestamp}@example.com`)

```bash
TEST_EMAIL="john.doe+$(date +%s)@example.com" pytest
```

## Page Object Model

The test suite uses the Page Object Model (POM) design pattern for better maintainability:

- **BasePage**: Common methods shared by all pages (find_element, wait_for_element, etc.)
- **HomePage**: Category navigation and search functionality
- **CategoryPage**: Product listing and navigation
- **ProductPage**: Product details and add to cart
- **SearchPage**: Search results (extends CategoryPage)
- **CartPage**: View cart, manage items
- **CheckoutPage**: Multi-step checkout (registration, address, delivery, payment)
- **ConfirmationPage**: Order confirmation and invoice download

## Download Directory

Test downloads (invoices) are saved to `./Resources/downloads/` by default, configurable through the `DOWNLOAD_PATH` in `config.py`.
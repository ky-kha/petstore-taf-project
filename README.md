# Pet Store API Test Automation Framework

A comprehensive Test Automation Framework (TAF) for validating the Swagger Petstore API endpoints. This project demonstrates professional test automation practices for API testing using Python and Pytest.

## Project Overview

This TAF implements automated testing for the key Pet Store API endpoints as specified in the requirements:
- **POST /pet** - Add a new pet to the store
- **GET /pet/{petId}** - Retrieve pet details by ID
- **PUT /pet** - Update an existing pet

## Framework Architecture

```
petstore-taf-project/
├── api/                    # API client layer
│   ├── __init__.py
│   └── pet_api.py          # PetApi wrapper with authentication
├── config/                 # Configuration files
│   └── config.yaml         # API base URL configuration
├── tests/                  # Test cases
│   ├── __init__.py
│   └── test_pet_api.py     # Main test suite
├── utils/                  # Test utilities
│   ├── __init__.py
│   └── data_generator.py   # Test data generation
├── .env                    # Environment variables (API keys)
├── conftest.py             # Pytest fixtures and configuration
├── pytest.ini              # Pytest settings
└── requirements.txt        # Project dependencies
```

## Technology Stack

- **Python 3.12+** - Core programming language
- **Pytest** - Testing framework
- **Requests** - HTTP client for API calls
- **PyYAML** - Configuration management
- **python-dotenv** - Environment variable management
- **pytest-html** - HTML test reports

## Authentication

The framework implements secure API key authentication as requested:
- API key configurable via environment file .env
- Stored securely in `.env` file
- Automatically included in all API requests via custom headers

## Getting Started

### Prerequisites
- Python 3.12 or higher
- Git

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd petstore-taf-project
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.template .env
   # Edit .env with your API key if different from default
   ```

### Running Tests

#### Run all tests:
```bash
pytest
```

#### Run with HTML report:
```bash
pytest --html=report.html --self-contained-html
```

#### Run specific test categories:
```bash
# Smoke tests only
pytest -m smoke

# Regression tests only
pytest -m regression

# Negative tests only
pytest -m negative

# One test example
python -m pytest tests/test_pet_api.py::TestPetAPI::test_get_pet_by_id -v -s


#### Run with verbose output:
```bash
pytest -v
```

## Test Coverage

The test suite includes comprehensive coverage of the required endpoints:

### POST /pet Tests
- ✅ Add pet with valid status values (available, pending, sold)
- ✅ Add pet with minimal required data
- ✅ Handle invalid data scenarios

### GET /pet/{petId} Tests
- ✅ Retrieve existing pet by ID
- ✅ Handle non-existent pet ID (error handling)
- ✅ Validate response structure and data integrity

### PUT /pet Tests
- ✅ Update existing pet information
- ✅ Handle non-existent pet updates
- ✅ Validate update operations

### Test Categories
- **Smoke Tests**: Core functionality validation
- **Regression Tests**: Update operations and edge cases
- **Negative Tests**: Error handling and invalid data scenarios

## Test Reporting

The framework generates detailed HTML reports with:
- Test execution summary
- Individual test results with logs
- Request/response details
- Execution timestamps
- Environment information

## Logging

Comprehensive logging is implemented throughout the framework:
- Setup and teardown operations
- API request/response details
- Test execution steps
- Error handling and debugging information

## Configuration

### Environment Variables
- `API_KEY`: API authentication key (documented)
- `LOG_LEVEL`: Logging level (default: INFO)
- `TEST_ENVIRONMENT`: Target environment (default: dev)

### Configuration Files
- `config/config.yaml`: Base API URL and settings
- `pytest.ini`: Pytest configuration and test markers
- `.env`: Environment-specific variables

## Test Data Management

Dynamic test data generation ensures:
- Unique pet names for each test run
- Realistic data structures
- Boundary value testing
- Invalid data scenarios for negative testing

## API Documentation

Reference: [Swagger Petstore API](https://petstore.swagger.io/)

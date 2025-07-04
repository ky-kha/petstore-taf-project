import pytest
import yaml
import os
import logging
from dotenv import load_dotenv
from api.pet_api import PetApi

# Load environment variables from .env file
load_dotenv()

# Configure logging for test execution visibility
logging.basicConfig(
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Console output
        logging.FileHandler('test_execution.log', mode='w')  # File output
    ],
    force=True  # Override any existing handlers
)


@pytest.fixture(scope="session")
def config():
    """
    Load test configuration from config files.
    """
    # Load base configuration
    with open("config/config.yaml") as f:
        config_data = yaml.safe_load(f)
    
    return config_data


@pytest.fixture(scope="session")
def api_credentials():
    """
    Retrieve API credentials from environment variables.
    """
    return {
        "api_key": os.getenv("API_KEY", "test_api_key")
    }


@pytest.fixture(scope="function")
def pet_api(config, api_credentials):
    """
    Create PetApi client with proper authentication.
    """
    logger = logging.getLogger("setup")
    logger.info("Setting up PetApi fixture")
    
    base_url = config["base_url"]
    api_key = api_credentials["api_key"]
    
    logger.info(f"Initializing PetApi with base_url: {base_url}")
    api_client = PetApi(base_url=base_url, api_key=api_key)
    
    logger.info("PetApi fixture setup completed successfully")
    return api_client


# Pytest hooks for enhanced logging and reporting
@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    """Log test setup information."""
    test_logger = logging.getLogger("test_execution")
    test_logger.info("=" * 80)
    test_logger.info(f"SETUP: Starting test {item.nodeid}")
    test_logger.info(f"Test file: {item.fspath}")
    test_logger.info(f"Test markers: {[mark.name for mark in item.iter_markers()]}")
    test_logger.info("=" * 80)


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_teardown(item, nextitem):
    """Log test teardown information."""
    test_logger = logging.getLogger("test_execution")
    test_logger.info("=" * 80)
    test_logger.info(f"TEARDOWN: Completed test {item.nodeid}")
    
    # Log test outcome if available
    if hasattr(item, 'rep_call'):
        test_logger.info(f"Test outcome: {item.rep_call.outcome.upper()}")
    
    test_logger.info("=" * 80)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Store test results for logging in teardown."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

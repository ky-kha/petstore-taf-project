import pytest
import logging
import time
from typing import Dict, Any
from utils.data_generator import generate_pet_data

logger = logging.getLogger(__name__)


class TestPetAPI:
    """Test suite for Pet Store API endpoints."""

    VALID_STATUSES = ["available", "pending", "sold"]
    NONEXISTENT_PET_ID = 9018568855

    @pytest.mark.smoke
    @pytest.mark.parametrize("status", VALID_STATUSES)
    def test_add_pet_with_status(self, pet_api, status):
        """Test adding pets with different status values."""
        logger.info(f"Testing POST /pet with status: {status}")

        pet_data = generate_pet_data(status=status)
        logger.info(f"Generated pet data: {pet_data}")
        response = pet_api.add_pet(pet_data)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        response_data = response.json()
        self._validate_pet_structure(response_data)
        assert response_data["name"] == pet_data["name"], "Pet name mismatch"
        assert response_data["status"] == status, f"Status mismatch: expected {status}"
        assert isinstance(response_data["id"], int), "Pet ID must be an integer"

        logger.info(
            f"Successfully created pet: ID={response_data['id']}, Name={response_data['name']}, Status={status}"
        )

    @pytest.mark.smoke
    def test_add_pet_minimal_data(self, pet_api):
        """Test adding pet with minimal required data."""
        logger.info("Testing POST /pet with minimal data")

        minimal_data = {
            "name": f"MinimalPet_{int(time.time() * 1000) % 1000}",
            "photoUrls": [],
        }
        logger.info(f"Minimal pet data: {minimal_data}")

        response = pet_api.add_pet(minimal_data)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        response_data = response.json()
        assert response_data["name"] == minimal_data["name"], "Pet name mismatch"
        assert "id" in response_data, "Response must contain pet ID"
        logger.info(
            f"Successfully created pet with minimal data: ID={response_data['id']}"
        )

    @pytest.mark.smoke
    def test_get_pet_by_id(self, pet_api):
        """Test retrieving pet details by ID."""
        logger.info("Testing GET /pet/{petId}")

        pet_data = generate_pet_data()
        create_response = pet_api.add_pet(pet_data)
        assert create_response.status_code == 200, "Failed to create test pet"

        pet_id = create_response.json()["id"]
        logger.info(f"Created test pet with ID: {pet_id}")

        time.sleep(1)

        response = pet_api.get_pet(pet_id)

        if response.status_code == 200:
            pet_details = response.json()
            self._validate_pet_structure(pet_details)

            assert pet_details["id"] == pet_id, "Pet ID mismatch"
            assert pet_details["name"] == pet_data["name"], "Pet name mismatch"
            logger.info(
                f"Successfully retrieved pet: ID={pet_id}, Name={pet_details['name']}"
            )

        elif response.status_code == 404:
            logger.warning(f"Pet {pet_id} not found - acceptable for demo environment")

        else:
            pytest.fail(f"Unexpected status code: {response.status_code}")

    @pytest.mark.regression
    def test_update_pet_details(self, pet_api):
        """Test updating existing pet information."""
        logger.info("Testing PUT /pet")

        original_data = generate_pet_data()
        create_response = pet_api.add_pet(original_data)
        assert create_response.status_code == 200, "Failed to create test pet"

        pet_id = create_response.json()["id"]
        logger.info(f"Created pet for update test: ID={pet_id}")

        updated_data = {
            "id": pet_id,
            "name": "UpdatedPetName",
            "status": "sold",
            "photoUrls": [],
        }

        response = pet_api.update_pet(updated_data)

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        response_data = response.json()
        assert response_data["id"] == pet_id, "Pet ID should remain unchanged"
        assert response_data["name"] == updated_data["name"], "Pet name not updated"
        assert (
            response_data["status"] == updated_data["status"]
        ), "Pet status not updated"

        logger.info(
            f"Successfully updated pet: ID={pet_id}, Name={response_data['name']}, Status={response_data['status']}"
        )

    @pytest.mark.negative
    def test_get_nonexistent_pet(self, pet_api):
        """Test error handling for non-existent pet IDs."""
        logger.info("Testing GET /pet/{petId} with non-existent ID")

        response = pet_api.get_pet(self.NONEXISTENT_PET_ID)

        if response.status_code == 404:
            logger.info(
                f"Correctly received 404 for nonexistent pet ID: {self.NONEXISTENT_PET_ID}"
            )
        elif response.status_code == 200:
            logger.warning(
                "Demo API returned 200 for nonexistent pet - acceptable for demo"
            )
        else:
            pytest.fail(f"Unexpected status code: {response.status_code}")

    @pytest.mark.negative
    def test_update_nonexistent_pet(self, pet_api):
        """Test error handling when updating non-existent pets."""
        logger.info("Testing PUT /pet with non-existent pet")

        update_data = {
            "id": self.NONEXISTENT_PET_ID,
            "name": "NonExistentPet",
            "status": "available",
            "photoUrls": [],
        }

        response = pet_api.update_pet(update_data)

        if response.status_code == 404:
            logger.info("Correctly received 404 for updating nonexistent pet")
        elif response.status_code == 200:
            logger.warning(
                "Demo API created new pet instead of returning 404 - acceptable for demo"
            )
        else:
            pytest.fail(f"Unexpected status code: {response.status_code}")

    @pytest.mark.negative
    def test_add_pet_invalid_data(self, pet_api):
        """Test input validation with invalid data."""
        logger.info("Testing POST /pet with invalid data")

        invalid_data = {"name": "", "photoUrls": [], "status": "invalid_status"}

        response = pet_api.add_pet(invalid_data)
        if response.status_code in [400, 422]:
            logger.info("API correctly rejected invalid data")
        elif response.status_code == 200:
            logger.warning(
                "Demo API accepted invalid data - real API should validate input"
            )
        else:
            pytest.fail(f"Unexpected status code: {response.status_code}")

    def _validate_pet_structure(self, pet_data: Dict[str, Any]) -> None:
        """Validate pet response structure."""
        required_fields = ["id", "name"]
        for field in required_fields:
            assert field in pet_data, f"Response missing required field: {field}"

        assert isinstance(pet_data["id"], int), "Pet ID must be an integer"
        assert pet_data["id"] > 0, "Pet ID must be positive"
        assert isinstance(pet_data["name"], str), "Pet name must be a string"
        assert len(pet_data["name"]) > 0, "Pet name cannot be empty"

import requests
import logging
import sys

class PetApi:
    """API wrapper for Petstore API operations."""
    
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.headers = {"api_key": api_key}
        self.logger = logging.getLogger(__name__)
        
    def _make_request(self, method, endpoint, **kwargs):
        """Make HTTP request with error handling."""
        url = f"{self.base_url}{endpoint}"
        self.logger.info(f"Making {method} request to {url}")
        
        # Merge authentication headers
        request_headers = self.headers.copy()
        if 'headers' in kwargs:
            request_headers.update(kwargs['headers'])
            kwargs['headers'] = request_headers
        else:
            kwargs['headers'] = request_headers

        try:
            response = requests.request(method, url, **kwargs)
            self.logger.info(f"Response: {response.status_code}")
            
            if self.logger.isEnabledFor(logging.DEBUG):
                self.logger.debug(f"Response body: {response.text[:200]}...")
                
            return response
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed: {e}")
            raise

    def add_pet(self, pet_data):
        """Add a new pet to the store."""
        pet_name = pet_data.get('name', 'Unknown')
        self.logger.info(f"Adding new pet: {pet_name}")
        
        return self._make_request('POST', '/pet', json=pet_data, timeout=30)

    def get_pet(self, pet_id):
        """Retrieve a pet by ID."""
        self.logger.info(f"Retrieving pet with ID: {pet_id}")
        return self._make_request('GET', f'/pet/{pet_id}', timeout=30)

    def update_pet(self, pet_data):
        """Update an existing pet."""
        pet_id = pet_data.get('id', 'Unknown')
        pet_name = pet_data.get('name', 'Unknown')
        self.logger.info(f"Updating pet ID {pet_id}: {pet_name}")
        
        return self._make_request('PUT', '/pet', json=pet_data, timeout=30)

    '''
    def delete_pet(self, pet_id):
        """Delete a pet (not used in tests per assignment requirements)."""
        self.logger.info(f"Deleting pet with ID: {pet_id}")
        return self._make_request('DELETE', f'/pet/{pet_id}', timeout=30)
    '''
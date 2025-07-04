#!/usr/bin/env python3

import requests
import json

def test_api_behavior():
    """Test the actual behavior of the Swagger Petstore API."""
    
    print("=== Testing Pet Creation and Retrieval ===")
    
    # Create a pet
    pet_data = {
        'name': 'DebugTestPet', 
        'photoUrls': [], 
        'status': 'available'
    }
    
    create_response = requests.post('https://petstore.swagger.io/v2/pet', json=pet_data)
    print(f"Create response: {create_response.status_code}")
    
    if create_response.status_code == 200:
        created_pet = create_response.json()
        pet_id = created_pet['id']
        print(f"Created pet ID: {pet_id}")
        print(f"Created pet name: {created_pet.get('name', 'N/A')}")
        
        # Try to get the pet immediately
        get_response = requests.get(f'https://petstore.swagger.io/v2/pet/{pet_id}')
        print(f"Get response (immediate): {get_response.status_code}")
        
        if get_response.status_code == 200:
            retrieved_pet = get_response.json()
            print(f"Retrieved pet name: {retrieved_pet.get('name', 'N/A')}")
            print(f"Retrieved pet ID: {retrieved_pet.get('id', 'N/A')}")
        else:
            print(f"Get failed: {get_response.text}")
    
    print("\n=== Testing Non-existent Pet ===")
    # Test with a clearly non-existent ID
    fake_id = 9999999999
    get_fake_response = requests.get(f'https://petstore.swagger.io/v2/pet/{fake_id}')
    print(f"Get fake pet response: {get_fake_response.status_code}")
    
    if get_fake_response.status_code == 200:
        fake_pet_data = get_fake_response.json()
        print(f"Fake pet data: {json.dumps(fake_pet_data, indent=2)}")
    else:
        print(f"Fake pet error: {get_fake_response.text}")
    
    print("\n=== Testing with ID that should exist ===")
    # Test with some IDs that might exist
    test_ids = [1, 2, 3, 10, 100]
    for test_id in test_ids:
        response = requests.get(f'https://petstore.swagger.io/v2/pet/{test_id}')
        if response.status_code == 200:
            pet_data = response.json()
            print(f"ID {test_id} exists: {pet_data.get('name', 'N/A')}")
        else:
            print(f"ID {test_id} does not exist (status: {response.status_code})")

if __name__ == "__main__":
    test_api_behavior()

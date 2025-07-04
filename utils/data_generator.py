import random

def generate_pet_data(name=None, status="available", category_name=None):
    """Generate realistic pet data for API testing."""
    pet_names = [
        "Srecko", "Miki", "Pas", "Rex", "Mica", 
        "Snoopy", "Micko", "Predrag", "Frndalo", "Bomboncic"
    ]
    categories = ["Dogs", "Cats", "Birds", "Fish", "Rabbits", "Hamsters"]
    
    pet_name = name or random.choice(pet_names)
    category = category_name or random.choice(categories)
    
    return {
        "id": random.randint(100000, 999999),
        "name": pet_name,
        "category": {
            "id": random.randint(1, 10),
            "name": category
        },
        "photoUrls": [
            f"https://example.com/photos/{pet_name.lower()}_1.jpg",
            f"https://example.com/photos/{pet_name.lower()}_2.jpg"
        ],
        "tags": [
            {
                "id": random.randint(1, 20),
                "name": f"tag_{random.randint(1, 100)}"
            }
        ],
        "status": status
    }
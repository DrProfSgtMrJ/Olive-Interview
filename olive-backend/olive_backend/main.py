from fastapi import FastAPI, HTTPException
from fastapi_pagination import Page, add_pagination, paginate
from fastapi.middleware.cors import CORSMiddleware
from .models import Dog, DogResponse
from dotenv import load_dotenv
import os
import requests

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

OLIVE_BASE_URL = os.getenv("OLIVE_DOG_BASE_URL")

@app.get("/dogs")
async def get_dogs(page: int, limit: int = 15) -> DogResponse:
    """
    Get a list of dogs with pagination.
    """
    total_dogs = 0
    current_page = page
    dogs = []
    while total_dogs <= limit:
        response = requests.get(OLIVE_BASE_URL, params={"page": current_page})
        if response.status_code != 200:
            break
        json_response = response.json()
        try:
            current_dogs = [Dog.from_json(dog) for dog in json_response]
            if not current_dogs:
                break

            remaining_slots = limit - total_dogs
            dogs_to_add = current_dogs[:remaining_slots]
            dogs.extend(dogs_to_add)
            total_dogs += len(dogs_to_add)
            current_page += 1
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing data: {str(e)}")
    
    next_page = current_page if current_page!= page else None
    dog_response = DogResponse(data=dogs, page=page, next_page=next_page, total=total_dogs)
    return dog_response 
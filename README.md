# Movie-Management-
Create a Movie Review &amp; Rec API integrating with The Movie Database API for movie data. Allow users to create, read, update, and delete reviews. Implement a rec system based on user reviews &amp; ratings. Include user auth &amp; RESTful API endpoints


## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/pankajtalwar/Movie-Management-

cd Movie-Management-
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
Access the project at http://127.0.0.1:8000/

## Example API Requests

### Create User

**Endpoint**: POST `/api/users/register/`

**Request Body**:
```json
{
  "username": "example",
  "email": "example@example.com",
  "password": "password123"
}

Response:
{
  "id": 1,
  "username": "example",
  "email": "example@example.com"
}

###############################################################

Get Movies
Endpoint: GET /api/users/movies/

Response:
[
  {
    "id": 1,
    "title": "Movie Title",
    "description": "Movie description",
    "release_date": "2024-01-01",
    "poster_url": "http://example.com/poster.jpg"
  }
]

################################################

## Postman Collection

You can import the Postman collection for this API [here](<link-to-postman-collection>).

###################################################################3333

## Postman Collection

import the Postman collection for this API from the following link:

- [Postman Collection](PostMan/Movie-Review-API.postman_collection.json)

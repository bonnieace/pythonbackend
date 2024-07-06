# Journal App

## Setup

1. Create a virtual environment and activate it.
2. Install the dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with your configuration.
4. Run the application: `uvicorn app.main:app --host 192.168.100.2 --port 8000`


# Journal App API Postman Collection

This Postman collection provides requests to interact with the backend of the Journal App. These requests demonstrate how to use various routes and interact with the API.

## Importing the Collection

1. Download the Postman collection JSON file 
2. Open Postman.
3. Click on **Import** in the top left corner.
4. Upload the downloaded JSON file.

## Requests

### Signup

This request adds user information to the database to facilitate authentication and separation of user interface logic.

```json
{
    "info": {
        "_postman_id": "2db83b9d-8aef-413a-b83b-06647644bbc6",
        "name": "Journal App API",
        "description": "Postman collection for the journal app. These requests help users interact with the backend and understand how routes are set up.",
        "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
        "_exporter_id": "30484198"
    },
    "item": [
        {
            "name": "Signup",
            "request": {
                "method": "POST",
                "header": [
                    {
                        "key": "Content-Type",
                        "value": "application/json"
                    }
                ],
                "body": {
                    "mode": "raw",
                    "raw": "{\"username\": \"johndoe\", \"password\": \"password\"}"
                },
                "url": {
                    "raw": "http://localhost:8000/signup",
                    "protocol": "http",
                    "host": [
                        "localhost"
                    ],
                    "port": "8000",
                    "path": [
                        "signup"
                    ]
                },
                "description": "This request adds user information to the database to ease with authentication and separation of user interface logic."
            },
            "response": []
        },
        {
            "name": "Login",
            "request": {
                "method": "POST",
                "header": [
                    {
                        "key": "Content-Type",
                        "value": "application/x-www-form-urlencoded"
                    }
                ],
                "body": {
                    "mode": "urlencoded",
                    "urlencoded": [
                        {
                            "key": "username",
                            "value": "johndoe"
                        },
                        {
                            "key": "password",
                            "value": "password"
                        }
                    ]
                },
                "url": {
                    "raw": "http://localhost:8000/token",
                    "protocol": "http",
                    "host": [
                        "localhost"
                    ],
                    "port": "8000",
                    "path": [
                        "token"
                    ]
                },
                "description": "This request authenticates users that are already signed up. It also provides a JSON web token for authorization."
            },
            "response": []
        },
        {
            "name": "Create Entry",
            "request": {
                "method": "POST",
                "header": [
                    {
                        "key": "Content-Type",
                        "value": "application/json"
                    },
                    {
                        "key": "Authorization",
                        "value": "Bearer {{access_token}}"
                    }
                ],
                "body": {
                    "mode": "raw",
                    "raw": "{\"title\": \"A new day\", \"content\": \"Started a new project\", \"category\": \"work\"}"
                },
                "url": {
                    "raw": "http://localhost:8000/entries",
                    "protocol": "http",
                    "host": [
                        "localhost"
                    ],
                    "port": "8000",
                    "path": [
                        "entries"
                    ]
                },
                "description": "This request is used to create a new journal entry."
            },
            "response": []
        },
        {
            "name": "Get Entries",
            "request": {
                "method": "GET",
                "header": [
                    {
                        "key": "Authorization",
                        "value": "Bearer {{access_token}}"
                    }
                ],
                "url": {
                    "raw": "http://localhost:8000/entries",
                    "protocol": "http",
                    "host": [
                        "localhost"
                    ],
                    "port": "8000",
                    "path": [
                        "entries"
                    ]
                },
                "description": "This request can be used to fetch all entries from the database. The request is user-specific, allowing users to only fetch their own data."
            },
            "response": []
        },
        {
            "name": "Update Entry",
            "request": {
                "method": "PUT",
                "header": [
                    {
                        "key": "Content-Type",
                        "value": "application/json"
                    },
                    {
                        "key": "Authorization",
                        "value": "Bearer {{access_token}}"
                    }
                ],
                "body": {
                    "mode": "raw",
                    "raw": "{\"title\": \"Updated day\", \"content\": \"Continued working on the project\", \"category\": \"work\"}"
                },
                "url": {
                    "raw": "http://localhost:8000/entries/1",
                    "protocol": "http",
                    "host": [
                        "localhost"
                    ],
                    "port": "8000",
                    "path": [
                        "entries",
                        "1"
                    ]
                },
                "description": "This request is used to update a specific entry using its ID."
            },
            "response": []
        },
        {
            "name": "Delete Entry",
            "request": {
                "method": "DELETE",
                "header": [
                    {
                        "key": "Authorization",
                        "value": "Bearer {{access_token}}"
                    }
                ],
                "url": {
                    "raw": "http://localhost:8000/entries/1",
                    "protocol": "http",
                    "host": [
                        "localhost"
                    ],
                    "port": "8000",
                    "path": [
                        "entries",
                        "1"
                    ]
                },
                "description": "This request is used to delete a specific entry using its ID."
            },
            "response": []
        }
    ]
}

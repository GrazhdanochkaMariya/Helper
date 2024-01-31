# Andersen Lead Generation Tool

Andersen Lead Generation Tool is a FastAPI-based application designed to streamline lead management processes for Andersen's lead generation department. Its primary functionalities include managing Google Sheets and providing a user-friendly interface for accessing APIs.

### Features

Admin panel: Users can efficiently manage records stored in database directly through the application's admin panel. This includes creating, updating, and deleting records as needed. The application allows users to export the entire database of data in CSV format for further analysis or external use.

Swagger API Documentation: The service is equipped with Swagger documentation, which provides users with a comprehensive overview of available APIs. Users can also generate new tokens for API access through Swagger.

Script for Database Updates: A script on the Google Sheets side is integrated with the service, allowing for automatic updates to the database based on incoming information. This script requires a token for authentication, which can be obtained through the API in Swagger in case of expiration.

## Technologies
- Python 3.11
- FastAPI==0.109.0
- Postgres 14.6
- Uvicorn
- Docker

## Setup
Please, follow steps to prepare project for local development:
1. Clone repository.
2. Setup venv with Python 3.11.
3. Install dependencies from requirements.txt file.
4. Create `.env` file from `.env.example`.
5. Setup database: `docker compose up -d`
6. Run migrations: `alembic upgrade head`
7. Initialise basic data: `python -m src.scripts.init_db` (create first admin user)
8. Install pre-commit hooks: `pre-commit install`
9. Run `uvicorn src.main:app --reload`

## Migrate database
1. Initialize migrations: `alembic revision --autogenerate -m "init"`
2. Make migrations: `alembic revision -m "<MSG>"`
3. Run migrations: `alembic upgrade head`

## APIs

1.Swagger: `http://127.0.0.1:8000/docs`. Log in with credentials that were created in database
- /api/check/contact/- API for cheking by LinkedIn profile if we have it in database.
  You can use it wherever you need: Swagger, Postman, plugin for browser. Pass in query params named "linkedin_profile" LinkedIn url when you use it. Returns contact data if contact exists in database. 
- /api/gs/changed - API for managing changes in Google Sheets. Available for request only with bearer token. Pass Bearer token to header "Authorization" of the request. Pass the contact data to the request body as JSON.The only valid statuses: DNM, CONTACT, DECLINED, REQUEST. Here are the fields:

```JSON
{

  "lead_name": "name_of_the_contact",

  "linkedin_profile": "contact_linkedin_profile",
  
  "next_contact": "date_of_next_contact",
  
  "status": "any_valid_status"
  
}
```

- /api/token - API for getting new token. Avaliable only in Swagger. Just execute it in Swagger. Returns a token valid for a year.

2.Admin Panel: `http://127.0.0.1:8000/admin`. Log in with credentials that were created in database
- Users Tab: You can edit, delete, create or export in CSV file admin users
- Lead Contacts Tab: you can search, edit, delete, create or export in CSV file contacts from database

## Developers

Yahor Vavilau (Tech Lead) - Contact: y.vavilau@andersenlab.com

Mariya Shakuro (Python Developer) - Contact: m.shakuro@andersenlab.com

# Invoice API

## About
This project was built for learning purposes as part of my Python portfolio. 
The goal was to understand how to design and build a REST API from scratch, 
structure it properly with separated concerns (endpoints vs database logic), 
secure it with authentication, and consume it from external applications such 
as Power Automate Desktop.

It demonstrates:
- Building and structuring a REST API with FastAPI
- Connecting an API to a database (migrated from CSV to SQLite)
- Securing endpoints with API Key authentication
- Using the API from external tools like Power Automate Desktop (run on local server)

## Tech Stack
- Python
- FastAPI
- SQLite
- Pydantic

## Project Structure
├── main.py          # API endpoints
├── database.py      # Database logic
├── invoices.db      # SQLite database (not included)
├── .env             # Secret keys (not included)
├── .env.example     # Environment variables template
└── requirements.txt # Project dependencies

## Setup
1. Clone the repository
2. Install dependencies (requirements.txt)
3. Create a `.env` file based on `.env.example`
4. Run the API using "uvicorn main:app --reload" command
5. Open the docs at `http://127.0.0.1:8000/docs`

## Authentication
All endpoints are protected with API Key authentication.
Add the header to every request 

## Endpoints
| Method | Endpoint | Description |
|---|---|---|
| GET | /invoices | Get all invoices |
| GET | /invoice/{invoice_id} | Get invoice by ID |
| POST | /invoice/create | Create new invoice |
| PATCH | /invoice/update/{invoice_id} | Update invoice |
| DELETE | /invoice/{invoice_id} | Delete invoice |
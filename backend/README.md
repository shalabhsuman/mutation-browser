# Backend API

This directory contains the Flask-based backend service for the Mutation Browser system.
The backend exposes a REST API for querying structured genomic mutation data stored
in a PostgreSQL database.

---

## Tech stack

- Python 3
- Flask
- psycopg2
- PostgreSQL
- Pytest
- Docker
- Docker Compose

---

## Project structure

- app.py  
  Flask application defining API endpoints

- requirements.txt  
  Python dependencies for the backend service

---

## Database configuration

The backend connects to a PostgreSQL database named `mutation_browser`.

When running with Docker Compose, database configuration is provided via environment
variables and service networking.

Default settings:
- Database name: mutation_browser
- Database port: 5432
- Database host: postgres (Docker Compose service name)

---

## Running locally without Docker (optional)

This mode is useful for development and debugging.

Activate the Conda environment:

conda activate mutation-browser

Install dependencies:

pip install -r requirements.txt

Run the Flask application:

python backend/app.py

The API will be available at:

http://localhost:5000

---

## Running with Docker Compose (recommended)

Docker Compose runs both the backend API and the PostgreSQL database.

From the project root, build and start services:

docker-compose up --build

The backend API will be available at:

http://localhost:8000

To stop services:

docker-compose down

---

## Docker-only workflow (backend image)

Build the backend Docker image manually:

docker build -t mutation-browser-api .

Run the container manually:

docker run -p 8000:5000 mutation-browser-api

---

## API endpoints

Health check:

GET /health

Response:

{"status": "ok"}

Query variants by gene:

GET /variants?gene=<GENE>

Returns a JSON array of mutation records for the specified gene.

---

## Testing

Unit tests are implemented using Pytest.

Run tests from the project root:

pytest

Tests cover:
- Health endpoint
- Input validation
- Variant query responses

---

## Development notes

- Flask debug mode is enabled for local development
- The backend service is stateless; all persistence is handled by PostgreSQL
- Database schema is defined in db/schema.sql at the project root

---

## Production considerations

For production deployments:
- Run the backend using Gunicorn instead of the Flask development server
- Deploy the containerized service using a container orchestrator (for example, AWS ECS)
- Use a managed PostgreSQL service (for example, AWS RDS)
- Disable Flask debug mode
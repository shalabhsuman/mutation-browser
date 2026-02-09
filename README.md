# Mutation Browser

Mutation Browser is a full-stack web application for storing, querying, and
interactively exploring structured genomic mutation data. The system combines
a relational database, a backend web API, a browser-based user interface, and
asynchronous query logging.

It is designed to demonstrate a clean, modular architecture for data ingestion,
persistence, asynchronous processing, and downstream consumption.

## Tech Stack

- **Frontend:** React, Vite
- **Backend:** Python, Flask, Flask-CORS, Gunicorn, Celery
- **Database:** PostgreSQL
- **Data Access:** psycopg2 (PostgreSQL driver)
- **Infra/DevOps:** Docker, Docker Compose, RabbitMQ
- **Architecture:** React frontend + Flask REST API + PostgreSQL database + async logging with Celery/RabbitMQ

---

## Overview

The Mutation Browser system provides:

- A PostgreSQL-backed data model for mutation records
- A batch ingestion mechanism for loading mutation data into the database
- A Flask-based web API for querying mutations
- A React-based frontend for interactive exploration
- Asynchronous logging of query events using Celery and RabbitMQ
- Background worker for audit and analytics tasks
- Containerized deployment using Docker and Docker Compose

The architecture cleanly separates data storage, application logic, and
presentation, and is suitable for local development as well as cloud deployment.

---

## Architecture

- Mutation records are stored in a PostgreSQL database.
- A Flask API queries the database using parameterized SQL.
- A React frontend consumes API responses over HTTP.
- A Celery worker consumes query-log tasks from RabbitMQ and writes to PostgreSQL.
- Services are orchestrated locally using Docker Compose.

<img src="docs/architecture.png" alt="Architecture diagram" height="500" width="600"/>

This diagram illustrates the flow of mutation data from ingestion through
persistent storage and into a stateless web API, which is then consumed by a
browser-based client.

---

## Project structure

- `backend/`  
  Flask web service implementing the API layer

- `backend/celery_app.py`  
  Celery app configuration and async task definitions

- `frontend/`  
  React application providing an interactive user interface

- `db/`  
  Database schema definitions

- `data/`  
  Data preparation and ingestion utilities

- `scripts/`  
  Operational and maintenance scripts

- `docker/`  
  Containerization documentation and assets
---

## Database schema

The database contains tables for mutation records and query logging:

**variants**
- `sample_id`
- `gene`
- `variant`
- `vaf`
- `tumor_type`

**query_events**
- `request_id`
- `gene`
- `requested_at`
- `status`

The schema is defined in `db/schema.sql`.

---



## API endpoints

- `GET /health`  
  Health check endpoint

- `GET /variants?gene=<GENE>`  
  Returns mutation records for the specified gene and a request ID

- `GET /status/<REQUEST_ID>`  
  Returns the async query-log status for a request ID

---

## User interface

The frontend provides a browser-based interface for querying mutation records
by gene name and inspecting results in tabular form, including a count of
matching samples.

The frontend communicates directly with the backend API and demonstrates
end-to-end data flow from database to user-facing application.

---

## Running the system locally

The backend API and database are run using Docker Compose, while the frontend
is served via a local development server.

At a high level:
1. Start backend services (API + Postgres + RabbitMQ + Celery):
   - `docker compose up -d`
2. Start the frontend dev server:
   - `cd frontend && npm run dev`
3. Open the app:
   - Frontend: http://localhost:5173
   - API: http://localhost:8000/health

Detailed run instructions are provided in the respective component directories.

---

## Async Request Flow (Query Logging)

1. User enters a gene in the React UI and clicks Search.
2. React calls `GET /variants?gene=<GENE>`.
3. Flask generates a `request_id` and enqueues a log task.
4. Flask queries Postgres and returns results immediately.
5. RabbitMQ delivers the queued task to the Celery worker.
6. The Celery worker writes a log row to `query_events`.
7. (Optional) `GET /status/<REQUEST_ID>` returns the log status.

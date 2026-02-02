# Mutation Browser

Mutation Browser is a backend system for storing and querying structured genomic
mutation data. The system consists of a relational database for persistence and
a web API for programmatic access to mutation records.

---

## Overview

The Mutation Browser system provides:

- A PostgreSQL-backed data model for mutation records
- A batch ingestion mechanism for loading mutation data into the database
- A Flask-based web API for querying mutations
- A clean separation between data storage, application logic, and presentation

The architecture is modular and designed to support extension, scaling, and
deployment to cloud environments.

---

## Architecture

- Mutation records are stored in a PostgreSQL database.
- A Flask API queries the database using parameterized SQL.
- Clients consume API responses over HTTP.

```mermaid
flowchart TD
  A[Mutation data\n(batch ingestion)] --> B[PostgreSQL\nvariants table]
  B --> C[Flask API\n/variants\n/health]
  C --> D[Clients\nCLI / Frontend]
  ```

This diagram illustrates the flow of mutation data from ingestion through
persistent storage and into a stateless web API consumed by downstream 

---

## Project structure

- `backend/`  
  Flask web service implementing the API layer

- `db/`  
  Database schema definitions

- `data/`  
  Data preparation and ingestion utilities

- `scripts/`  
  Operational and maintenance scripts

- `frontend/`  
  Frontend application

- `docker/`  
  Containerization assets
---

## Database schema

The database contains a single table for mutation records:

**variants**
- `sample_id`
- `gene`
- `variant`
- `vaf`
- `tumor_type`

The schema is defined in `db/schema.sql`.

---



## API endpoints

- `GET /health`  
  Health check endpoint

- `GET /variants?gene=<GENE>`  
  Returns mutation records for the specified gene as JSON
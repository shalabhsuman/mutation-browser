# Frontend

This directory contains the React-based user interface for the Mutation Browser system.
The frontend provides a simple search interface for querying mutation records from the backend API.

The application is built using React and Vite and communicates with the backend over HTTP.

---

## Tech stack

- React
- Vite
- JavaScript (ES modules)
- Fetch API for backend communication

---

## Prerequisites

- Node.js (includes npm)

Verify installation:

node --version  
npm --version

---

## Project creation

The frontend was scaffolded using Vite with the following command:

npm create vite@latest .

During setup:
- Framework: React
- Variant: JavaScript

---

## Dependency installation

Install project dependencies:

npm install

---

## Running the development server

Start the Vite development server:

npm run dev

The frontend will be available at:

http://localhost:5173

---

## Backend integration

The frontend communicates with the backend API at:

http://localhost:8000

Ensure the backend service is running (via Docker Compose or locally) before using the frontend.

Example API endpoint used by the UI:

GET /variants?gene=TP53

---

## Development notes

- The Vite dev server runs independently from Docker
- Hot Module Replacement (HMR) is enabled by default
- API requests are made directly to the backend service

---

## Production build

To generate a production build:

npm run build

This creates a dist/ directory containing static assets suitable for deployment to a static hosting service
(for example, S3 and CloudFront on AWS).
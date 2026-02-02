---

## Database setup when running PostgreSQL in Docker

This section documents how to interact with the PostgreSQL database when it is
running inside a Docker container (for example, via Docker Compose).

---

### Identify the PostgreSQL container

List running containers:

docker ps

Locate the PostgreSQL container name (for example):

mutation-browser-postgres

---

### Access PostgreSQL inside the container

Open a shell inside the Postgres container:

docker exec -it mutation-browser-postgres bash

Once inside the container, connect to PostgreSQL:

psql -U postgres

---

### Create the application database

Create the database:

CREATE DATABASE mutation_browser;

Exit psql:

\q

---

### Connect to the application database

psql -U postgres mutation_browser

---

### Create schema inside the container

Run the schema file from within the container:

\i /docker-entrypoint-initdb.d/schema.sql

Verify the table exists:

\d variants

---

### Load CSV data into the container database

Copy the CSV file into the container:

docker cp data/mutations.csv mutation-browser-postgres:/tmp/mutations.csv

Load the data:

\copy variants(sample_id, gene, variant, vaf, tumor_type)
FROM '/tmp/mutations.csv'
DELIMITER ','
CSV HEADER;

---

### Verify data inside the container

Check row count:

SELECT COUNT(*) FROM variants;

Example query:

SELECT * FROM variants WHERE gene = 'TP53' LIMIT 5;

---

## Exporting and importing database data

### Export database from Docker container

Create a database dump:

docker exec mutation-browser-postgres pg_dump -U postgres mutation_browser > mutation_browser.sql

---

### Import database into Docker container

Copy the dump file into the container:

docker cp mutation_browser.sql mutation-browser-postgres:/tmp/mutation_browser.sql

Restore the database:

docker exec -it mutation-browser-postgres psql -U postgres mutation_browser -f /tmp/mutation_browser.sql

---

### Notes

- Docker volumes preserve database state across container restarts
- Exporting with pg_dump is the preferred way to move databases between systems
- The same import/export approach applies when migrating to managed databases
  (for example, AWS RDS)
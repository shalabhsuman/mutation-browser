CREATE TABLE variants (
  id SERIAL PRIMARY KEY,
  sample_id TEXT NOT NULL,
  gene TEXT NOT NULL,
  variant TEXT NOT NULL,
  vaf FLOAT,
  tumor_type TEXT
);

CREATE TABLE query_events (
  id SERIAL PRIMARY KEY,
  request_id TEXT NOT NULL UNIQUE,
  gene TEXT NOT NULL,
  requested_at TIMESTAMPTZ NOT NULL,
  status TEXT NOT NULL
);

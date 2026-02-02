CREATE TABLE variants (
  id SERIAL PRIMARY KEY,
  sample_id TEXT NOT NULL,
  gene TEXT NOT NULL,
  variant TEXT NOT NULL,
  vaf FLOAT,
  tumor_type TEXT
);

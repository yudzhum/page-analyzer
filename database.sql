DROP TABLE IF EXISTS urls;
DROP TABLE IF EXISTS url_checks;

CREATE TABLE urls (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) UNIQUE NOT NULL,
  created_at DATE NOT NULL
);
CREATE TABLE url_checks (
  id SERIAL PRIMARY KEY,
  url_id bigint REFERENCES urls(id),
  status_code integer NOT NULL,
  h1 VARCHAR(255),
  title text,
  description text,
  created_at DATE NOT NULL
);

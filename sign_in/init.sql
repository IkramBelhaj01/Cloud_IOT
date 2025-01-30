CREATE DATABASE db_ms;

\c db_ms;

CREATE TABLE IF NOT EXISTS T_USER (
    id SERIAL PRIMARY KEY,
    email VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

INSERT INTO T_USER (email, password) VALUES ('esisa@esisa.ac.ma', '1234');
INSERT INTO T_USER (email, password) VALUES ('test@esisa.ac.ma', '1234');

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE operations (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50),
    type VARCHAR(50) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
	category VARCHAR(50),
    year INT NOT NULL,
    month INT NOT NULL CHECK (month BETWEEN 1 AND 12)
);


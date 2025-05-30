CREATE TABLE IF NOT EXISTS aggregated_transaction (
    id SERIAL PRIMARY KEY,
    country TEXT NOT NULL,
    state TEXT,
    year INTEGER NOT NULL,
    name TEXT NOT NULL,
    count BIGINT NOT NULL,
    amount DOUBLE PRECISION NOT NULL
);


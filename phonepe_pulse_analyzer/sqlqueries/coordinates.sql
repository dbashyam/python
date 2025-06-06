CREATE TABLE state_coordinates (
    state TEXT PRIMARY KEY,
    latitude FLOAT,
    longitude FLOAT
);

-- Example insert
INSERT INTO state_coordinates (state, latitude, longitude) VALUES
('Tamil Nadu', 11.1271, 78.6569),
('Maharashtra', 19.7515, 75.7139)
-- Add all states...
;

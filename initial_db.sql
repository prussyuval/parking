create database parking;

create table if not exists parking_lots (
    id SERIAL PRIMARY KEY,
    lot_id INT NOT NULL,
    day INT NOT NULL,
    hour INT NOT NULL,
    minute INT NOT NULL,
    status JSONB
);
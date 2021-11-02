create database parking;

create table if not exists parking_lots (
    id int PRIMARY KEY,
    day int NOT NULL,
    hour int NOT NULL,
    minute int NOT NULL,
    status JSONB
);
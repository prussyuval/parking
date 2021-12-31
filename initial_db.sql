create database parking;

create table if not exists parking_lots (
    id SERIAL PRIMARY KEY,
    lot_id INT NOT NULL,
    day INT NOT NULL,
    hour INT NOT NULL,
    minute INT NOT NULL,
    status JSONB
);

create table if not exists lots (
  id SERIAL PRIMARY KEY,
  lot_id INT NOT NULL,
  eng_name TEXT NOT NULL,
  heb_name TEXT NOT NULL,
  address TEXT NOT NULL,
  nicknames JSONB
);

create table if not exists traffic (
    ip SERIAL PRIMARY KEY,
    entrances int default 0
);

create table if not exists parking_lot_views (
    id SERIAL PRIMARY KEY,
    lot_id INT NOT NULL,
    heat_map_data JSONB
);

INSERT INTO lots (lot_id, eng_name, heb_name, address, nicknames) VALUES (40, 'ravnitzky', 'רבניצקי', 'רבניצקי 6 תל-אביב יפו', '[]');
INSERT INTO lots (lot_id, eng_name, heb_name, address, nicknames) VALUES (94, 'habima plaza', 'התרבות', ' הוברמן 1 תל-אביב יפו', '["הבימה"]');
INSERT INTO lots (lot_id, eng_name, heb_name, address, nicknames) VALUES (45, 'tel nordau', 'תל-נורדאו', 'פרישמן 28 תל-אביב יפו', '[]');

INSERT INTO lots (lot_id, eng_name, heb_name, address, nicknames) VALUES (31, 'Da Vinci ', 'מפעל הפיס', 'ליאונרדו דוינצי 5 תל-אביב יפו', '["Hapais"]');

-- ALTER TABLE parking_lots ADD COLUMN update_date timestamp;
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

INSERT INTO lots (lot_id, eng_name, heb_name, address, nicknames) VALUES (29, 'montefiore', 'מונטיפיורי', 'מונטיפיורי 5 תל-אביב יפו', '[]');
INSERT INTO lots (lot_id, eng_name, heb_name, address, nicknames) VALUES (10, 'golda', 'גולדה', 'ברקוביץ 7 תל-אביב יפו', '[]');
INSERT INTO lots (lot_id, eng_name, heb_name, address, nicknames) VALUES (123, 'arlosoroff', 'ארלוזורוב 17', 'ארלוזורוב 17 תל-אביב יפו', '["חיים ארלוזורוב"]');
INSERT INTO lots (lot_id, eng_name, heb_name, address, nicknames) VALUES (122, 'assuta', 'אסותא', ' ז`בוטינסקי 62 תל-אביב יפו', '["אסותה"]');
INSERT INTO lots (lot_id, eng_name, heb_name, address, nicknames) VALUES (3, 'basel', 'באזל', 'אשתורי הפרחי 5 תל-אביב יפו', '["באסל"]');
INSERT INTO lots (lot_id, eng_name, heb_name, address, nicknames) VALUES (37, 'cinerama', 'סינרמה', 'יצחק שדה 45 תל-אביב יפו', '["סינרמא"]');

INSERT INTO lots (lot_id, eng_name, heb_name, address, nicknames) VALUES (31, 'da vinci ', 'מפעל הפיס', 'ליאונרדו דוינצי 5 תל-אביב יפו', '["Hapais"]');

INSERT INTO lots (lot_id, eng_name, heb_name, address, nicknames) VALUES (4, 'hevra hadasha', 'חברה חדשה', 'חברה חדשה 9 תל-אביב יפו', '[]');
INSERT INTO lots (lot_id, eng_name, heb_name, address, nicknames) VALUES (39, 'palmach', 'פלמ״ח', ' יגאל אלון 68 תל-אביב יפו', '["יגאל אלון"]');
INSERT INTO lots (lot_id, eng_name, heb_name, address, nicknames) VALUES (19, 'ha-tsfira', 'הצפירה 1', ' הצפירה 2 תל-אביב יפו', '["ha tsfira"]');
INSERT INTO lots (lot_id, eng_name, heb_name, address, nicknames) VALUES (38, 'saadia gaon', 'סעדיה גאון', 'ציקלג 7 תל-אביב יפו', '[]');


-- ALTER TABLE parking_lots ADD COLUMN update_date timestamp;
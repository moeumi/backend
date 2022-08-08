DROP TABLE IF EXISTS contents;
DROP TABLE IF EXISTS city;
DROP TABLE IF EXISTS district;
DROP TABLE IF EXISTS center;
DROP TABLE IF EXISTS category;
DROP TABLE IF EXISTS apply_state;
DROP TABLE IF EXISTS test_contents;
DROP TABLE IF EXISTS logo;

CREATE table test_contents
(
    center_name        TEXT NOT NULL,
    contents_title     TEXT NOT NULL,
    contents_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    category           TEXT,
    detail_link        TEXT,
    apply_start_date   TEXT, /*YYYY-MM-DD*/
    apply_end_date     TEXT,
    operate_start_date TEXT,
    operate_end_date   TEXT,
    edu_target         TEXT,
    apply_target       TEXT,
    max_apply_num      INTEGER,
    applied_num        INTEGER,
    wait_num           INTEGER,
    apply_state        TEXT,
    FOREIGN KEY ("category") REFERENCES category("category"),
    FOREIGN KEY ("center_name") REFERENCES center("center_name"),
    FOREIGN KEY ("apply_state") REFERENCES apply_state("apply_state")
);

CREATE table contents
(
    center_name        TEXT NOT NULL,
    contents_title     TEXT NOT NULL,
    contents_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    category           TEXT,
    detail_link        TEXT,
    apply_start_date   TEXT, /*YYYY-MM-DD*/
    apply_end_date     TEXT,
    operate_start_date TEXT,
    operate_end_date   TEXT,
    edu_target         TEXT,
    apply_target       TEXT,
    max_apply_num      INTEGER,
    applied_num        INTEGER,
    wait_num           INTEGER,
    apply_state        TEXT,
    FOREIGN KEY ("category") REFERENCES category("category"),
    FOREIGN KEY ("center_name") REFERENCES center("center_name"),
    FOREIGN KEY ("apply_state") REFERENCES apply_state("apply_state")
);

CREATE table city
(
    city_name TEXT PRIMARY_KEY
);
INSERT OR IGNORE INTO city VALUES ('부산광역시');

CREATE table district
(
    city_name     TEXT,
    district_name TEXT PRIMARY KEY,
    FOREIGN KEY("city_name") REFERENCES city("city_name")
);
INSERT OR IGNORE INTO district VALUES(('부산광역시','중구'),('부산광역시','서구'),
    ('부산광역시','동구'),('부산광역시','영도구'),('부산광역시','부산진구'),('부산광역시','동래구'),
    ('부산광역시','남구'),('부산광역시','북구'),('부산광역시','해운대구'),('부산광역시','사하구'),
    ('부산광역시','금정구'),('부산광역시','강서구'),('부산광역시','연제구'),('부산광역시','수영구'),
    ('부산광역시','사상구'),('부산광역시','기장군'));

CREATE table center
(
    city_name     TEXT,
    district_name TEXT,
    center_name   TEXT PRIMARY KEY,
    FOREIGN KEY("city_name") REFERENCES city("city_name"),
    FOREIGN KEY("district_name") REFERENCES district("district_name")
);


CREATE table category
(
    category TEXT PRIMARY KEY
);
/*INSERT INTO category values();*/

CREATE table apply_state
(
    apply_state TEXT PRIMARY KEY /*접수중, 마감, 대기접수, 예정*/
);

INSERT OR IGNORE INTO apply_state VALUES (('접수중'),('마감'),('대기접수'),('예정'),('대기중'),('접수마감') );

CREATE table logo
(
    image_link TEXT
);



DROP TABLE IF EXISTS contents;
DROP TABLE IF EXISTS city;
DROP TABLE IF EXISTS district;
DROP TABLE IF EXISTS center;
DROP TABLE IF EXISTS category;
DROP TABLE IF EXISTS apply_state;
DROP TABLE IF EXISTS test_contents;
DROP TABLE IF EXISTS test_center;
DROP TABLE IF EXISTS test_placement;
DROP TABLE IF EXISTS test_category;
DROP TABLE IF EXISTS logo;

CREATE table test_contents
(
    center_name        TEXT NOT NULL,
    placement_name     TEXT,
    contents_title     TEXT NOT NULL,
    contents_id        INTEGER,
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
    CONSTRAINT contents_pk PRIMARY KEY (center_name, contents_id, contents_title),
    FOREIGN KEY ("placement_name") REFERENCES placement("placement_name"),
    FOREIGN KEY ("category") REFERENCES category("category"),
    FOREIGN KEY ("center_name") REFERENCES center("center_name"),
    FOREIGN KEY ("apply_state") REFERENCES apply_state("apply_state")
);

CREATE table contents
(
    center_name        TEXT NOT NULL,
    placement_name     TEXT,
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
INSERT OR IGNORE INTO city VALUES ('???????????????');

CREATE table district
(
    city_name     TEXT,
    district_name TEXT PRIMARY KEY,
    FOREIGN KEY("city_name") REFERENCES city("city_name")
);

INSERT OR IGNORE INTO district(city_name, district_name) VALUES ('???????????????','??????');
INSERT OR IGNORE INTO district(city_name, district_name) VALUES ('???????????????','??????');
INSERT OR IGNORE INTO district(city_name, district_name) VALUES ('???????????????','??????');
INSERT OR IGNORE INTO district(city_name, district_name) VALUES ('???????????????','?????????');
INSERT OR IGNORE INTO district(city_name, district_name) VALUES ('???????????????','????????????');
INSERT OR IGNORE INTO district(city_name, district_name) VALUES ('???????????????','?????????');
INSERT OR IGNORE INTO district(city_name, district_name) VALUES ('???????????????','??????');
INSERT OR IGNORE INTO district(city_name, district_name) VALUES ('???????????????','??????');
INSERT OR IGNORE INTO district(city_name, district_name) VALUES ('???????????????','????????????');
INSERT OR IGNORE INTO district(city_name, district_name) VALUES ('???????????????','?????????');
INSERT OR IGNORE INTO district(city_name, district_name) VALUES ('???????????????','?????????');
INSERT OR IGNORE INTO district(city_name, district_name) VALUES ('???????????????','?????????');
INSERT OR IGNORE INTO district(city_name, district_name) VALUES ('???????????????','?????????');
INSERT OR IGNORE INTO district(city_name, district_name) VALUES ('???????????????','?????????');
INSERT OR IGNORE INTO district(city_name, district_name) VALUES ('???????????????','?????????');
INSERT OR IGNORE INTO district(city_name, district_name) VALUES ('???????????????','?????????');

CREATE table center
(
    city_name     TEXT,
    district_name TEXT,
    center_name   TEXT PRIMARY KEY,
    FOREIGN KEY("city_name") REFERENCES city("city_name"),
    FOREIGN KEY("district_name") REFERENCES district("district_name")
);

CREATE table test_center
(
    city_name     TEXT,
    district_name TEXT,
    center_name   TEXT PRIMARY KEY,
    FOREIGN KEY("city_name") REFERENCES city("city_name"),
    FOREIGN KEY("district_name") REFERENCES district("district_name")
);

CREATE table test_placement
(
    center_name   TEXT,
    placement_name TEXT PRIMARY KEY,
    FOREIGN KEY("center_name") REFERENCES test_center("center_name")
);


CREATE table test_category
(
    main_category TEXT,
    category TEXT PRIMARY KEY
);


/*INSERT INTO category values();*/

CREATE table apply_state
(
    apply_state TEXT PRIMARY KEY /*?????????, ??????, ????????????, ??????*/
);

INSERT OR IGNORE INTO apply_state VALUES ('?????????');
INSERT OR IGNORE INTO apply_state VALUES ('??????');
INSERT OR IGNORE INTO apply_state VALUES ('????????????');
INSERT OR IGNORE INTO apply_state VALUES ('??????');
INSERT OR IGNORE INTO apply_state VALUES ('?????????');
INSERT OR IGNORE INTO apply_state VALUES ('????????????');

CREATE table logo
(
    image_link TEXT
);

CREATE TABLE sex(
    sex TEXT PRIMARY KEY
);
insert or ignore into sex(sex) values("??????");
insert or ignore into sex(sex) values("??????");
insert or ignore into sex(sex) values("????????????");

CREATE TABLE age(
    age TEXT PRIMARY KEY
);
insert or ignore into age(age) values("10");
insert or ignore into age(age) values("20");
insert or ignore into age(age) values("30");
insert or ignore into age(age) values("40");
insert or ignore into age(age) values("50+");

CREATE TABLE user(
    token TEXT PRIMARY KEY,
    sex TEXT,
    age TEXT,
    FOREIGN KEY ("sex") REFERENCES sex("sex"),
    FOREIGN KEY ("age") REFERENCES age("age"),
);

CREATE TABLE test_user_category(
    token   TEXT,
    category    TEXT,
    CONSTRAINT category_user_pk PRIMARY KEY (token, category),
    FOREIGN KEY ("token") REFERENCES user("token"),
);



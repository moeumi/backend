DROP TABLE IF EXISTS contents;
DROP TABLE IF EXISTS city;
DROP TABLE IF EXISTS district;
DROP TABLE IF EXISTS center;
DROP TABLE IF EXISTS category;
DROP TABLE IF EXISTS apply_state;

CREATE table contents{
    center_name TEXT NOT NULL,
    contents_title TEXT NOT NULL,
    contents_id TEXT NOT NULL PRIMARY_KEY AUTOINCREMENT,
    category TEXT,
    detail_link TEXT,
    apply_start_date TEXT, /*YYYY-MM-DD*/
    apply_end_date TEXT,
    operate_start_date TEXT,
    operate_end_date TEXT,
    edu_target TEXT,
    apply_target TEXT,
    max_apply_num INTEGER,
    applied_num INTEGER,
    wait_num INTEGER,
    apply_state TEXT,
    FOREIGN KEY("category") REFERENCE category("category"),
    FOREIGN KEY("center_name") REFERENCE center("center_name"),
    FOREIGN KEY("apply_state") REFERENCE apply_state("apply_state")
};

CREATE table city{
    city_name TEXT PRIMARY_KEY
}

CREATE table district{
    city_name TEXT,
    district_name TEXT PRIMARY_KEY,
    FOREIGN_KEY("city_name") REFERENCE city("city_name")
}

CREATE table center{
    city_name TEXT,
    district_name TEXT,
    center_name TEXT PRIMARY_KEY,
    FOREIGN_KEY("city_name") REFERENCE city("city_name"),
    FOREIGN_KEY("district_name") REFERENCE district("district_name")
}

CREATE table category{
    category TEXT PRIMARY_KEY
}

CREATE table apply_state{
    apply_state TEXT PRIMARY_KEY /*접수중, 마감, 대기접수, 예정*/
}




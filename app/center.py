import json

import pandas as pd
import os.path
from app.db import get_db
from PyKakao import KakaoLocal


def center():
    db = get_db()
    base_path = os.path.dirname(__file__)
    df = pd.read_excel(os.path.join(base_path,'../data/시설.xlsx'), header=None, index_col=None)
    lists = [[df[0][i], df[1][i]] for i in range(len(df))]
    cur=db.cursor()
    for i in range(len(lists)):
        cur.execute("insert or ignore into test_center(city_name, district_name, center_name) values (?,?,?);",
                    ('부산광역시', lists[i][1], lists[i][0]))
    db.commit()


def center_lat_log():
    db = get_db()
    base_path = os.path.dirname(__file__)
    with open(os.path.join(base_path, '../config.json')) as json_file:
        json_data = json.load(json_file)
        key = json_data['REST_KEY']
    KL = KakaoLocal(key)
    cur = db.cursor()
    results = cur.execute(
        "SELECT real_placement_name FROM test_placement_loc"
    ).fetchall()
    for result in results:
        tmp = KL.search_keyword(query=result[0])["documents"][0]
        cur.execute("UPDATE test_placement_loc SET longitude=:log, latitude=:lat WHERE real_placement_name = :real;", {'log':tmp['x'], 'lat':tmp['y'], 'real':result[0]})
    db.commit()

if __name__=="__main___":
    center()

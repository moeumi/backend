
import pandas as pd
import os.path
from app.db import get_db


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



if __name__=="__main___":
    center()

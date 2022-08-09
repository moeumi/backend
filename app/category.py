
import pandas as pd
import os.path
from werkzeug.local import LocalProxy

from app.db import get_db

def category():
    base_path = os.path.dirname(__file__)
    df = pd.read_excel(os.path.join(base_path,'../data/분류표.xlsx'))
    db = LocalProxy(get_db)
    #lists = [[df[0][i], df[1][i]] for i in range(len(df))]
    #cur=db.cursor()
    #for i in df.keys():
    #    cur.execute("insert or ignore into center(main_category, sub_category) values (?,?);",
    #                ('공예', df['공예'][0]))
    cur = db.cursor()
    for i in df.keys():
        cur.execute("insert or ignore into test_category(category) values (?)", (i,))
    db.commit()


if __name__=="__main___":
    category()

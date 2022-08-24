
import pandas as pd
import os.path
from app.db import get_db

def auto_category():
    base_path = os.path.dirname(__file__)
    df = pd.read_excel(os.path.join(base_path,"contents.xlsx"))

    category = pd.read_excel(os.path.join(base_path,"category.xlsx"))
    category_size = category.columns.size

    count = df["제목"].value_counts().count()
    df["분류"] = ""

    for x in range(0, category_size):
        for y in range(0, category[category.columns[x]].value_counts().count()):
            for i in range(0, count):
                if (category[category.columns[x]].iloc[y] in df["제목"].iloc[i]):

                    if (category.columns[x] not in df["분류"].iloc[i]):
                        if (len(df["분류"].iloc[i]) == 0):
                            df["분류"].iloc[i] += category.columns[x]
                        else:
                            df["분류"].iloc[i] += ","
                            df["분류"].iloc[i] += category.columns[x]
    for i in range(0, count):
        if (len(df["분류"].iloc[i]) == 0):
            df["분류"].iloc[i] += "기타"

    df.to_excel("output.xlsx")
def category():
    base_path = os.path.dirname(__file__)
    df = pd.read_excel(os.path.join(base_path,'../data/분류표.xlsx'))
    db = get_db()
    cur = db.cursor()
    for i in df.keys():
        cur.execute("insert or ignore into test_category(category) values (?)", (i,))
    db.commit()


if __name__=="__main___":
    category()

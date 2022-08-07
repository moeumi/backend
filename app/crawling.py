import json

import pandas as pd
from app.db import get_db
import requests
from bs4 import BeautifulSoup as bs
from flask import Blueprint, jsonify

bp = Blueprint("app", __name__)


@bp.route("/testdb")
def busan_lib_event():
    busan_lib_event_url = "https://home.pen.go.kr/yeyak/edu/lib/selectEduList.do?mi=14556&eduSeq=&srchRsSysId=&srchEduCtgry=&currPage=1&srchRsvSttus=&srchPeriodDiv=rcept&srchRsvBgnde=&srchRsvEndde=&srchRsvValue=&pageIndex=50"
    busan_lib_event = pd.read_html(busan_lib_event_url)
    busan_lib_event = busan_lib_event[0]
    for classify in busan_lib_event:
        if classify == "기관명":
            busan_lib_event[classify] = busan_lib_event[classify].str.split("  ").str[1]
        if classify == "교육명":
            busan_lib_event[classify] = busan_lib_event[classify].str.split("]  ", 1).str[1]
        if classify == "운영기간" or classify == "접수기간" or classify == "교육대상" or classify == "신청대상":
            busan_lib_event[classify] = busan_lib_event[classify].str.split("  ", 1).str[1:].str[0]
        if classify == "모집인원":
            busan_lib_event[classify] = busan_lib_event[classify].str.split("  ", 2).str[2]

    request = requests.get(
        "https://home.pen.go.kr/yeyak/edu/lib/selectEduList.do?mi=14556&eduSeq=&srchRsSysId=&srchEduCtgry=&currPage=1&srchRsvSttus=&srchPeriodDiv=rcept&srchRsvBgnde=&srchRsvEndde=&srchRsvValue=&pageIndex=50")
    soup = bs(request.content, "html.parser")
    table = soup.findAll("a", class_="viewEduInfo")

    libraries = soup.select("ul.tabList>li>a")[1:]
    library_dict = {}
    for library in libraries:
        tmp = str(library).split('data-id="')[1].split("\"")
        library_dict[library.string] = tmp[0]

    elements = list(soup.select("a.viewEduInfo"))
    element_list = []
    for element in elements:
        tmp = str(element).split('class="')[1].split("\"")
        if tmp[0] == "viewEduInfo":
            element_list.append(tmp[4])  # edu-se,data-id(edu-seq)

    db = get_db()
    cur = db.cursor()

    for row in busan_lib_event.itertuples():
        detail_link = ('https://home.pen.go.kr/yeyak/edu/lib/selectEduInfo.do?mi=14460&eduSeq='
        + element_list[row[0]]+'&srchRsSysId='+library_dict[row[2]])
        cur.execute("insert into test_contents(center_name, contents_title, category, detail_link,"
                    "apply_start_date, apply_end_date, operate_start_date, operate_end_date,"
                    "edu_target,apply_target,max_apply_num,applied_num,wait_num,apply_state) values"
                    "(?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (row[2], row[3], 'none', detail_link,
                                                      row[4].split(" ~")[0], row[4].split(" ~")[1],
                                                      row[5].split(" ~")[0], row[5].split(" ~")[1],
                                                      row[6], row[7],
                                                      int(row[8].split("/")[0].split(":")[1].strip("명")),
                                                      int(row[8].split("/")[1].split(":")[1].split("명")[0]),
                                                      0, row[9])
                    )
    db.commit()
    db.close()

    return "finish"

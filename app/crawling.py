import json

import pandas as pd
from app.db import get_db
import requests
from bs4 import BeautifulSoup as bs
from flask import Blueprint, jsonify

bp = Blueprint("app", __name__)


@bp.route("/testdb/busan_lib_event")
def busan_lib_event():
    db = get_db()
    for i in range(1,5):
        busan_lib_event_url = "https://home.pen.go.kr/yeyak/edu/lib/selectEduList.do?mi=14556&eduSeq=&srchRsSysId=&srchEduCtgry=&currPage="+str(i)+"&srchRsvSttus=&srchPeriodDiv=rcept&srchRsvBgnde=&srchRsvEndde=&srchRsvValue=&pageIndex=50"
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

        request = requests.get(busan_lib_event_url)
        soup = bs(request.content, "html.parser")
        table = soup.findAll("a", class_="viewEduInfo")

        libraries = soup.select("ul.tabList>li>a")[1:]
        library_dict = {}
        for library in libraries:
            tmp = str(library).split('data-id="')[1].split("\"")
            library_dict[library.string] = tmp[0]

        elements = list(soup.select("a.viewEduInfo"))
        element_list = []
        element_str_list = []
        for element in elements:
            tmp = str(element).split('class="')[1].split("\"")
            if tmp[0] == "viewEduInfo":
                element_list.append(tmp[4])  # edu-se,data-id(edu-seq)
                element_str_list.append(element.string)


        cur = db.cursor()

        for row in busan_lib_event.itertuples():
            tmp_row = row[0]
            detail_link = ('https://home.pen.go.kr/yeyak/edu/lib/selectEduInfo.do?mi=14460&eduSeq='
            + element_list[tmp_row]+'&srchRsSysId='+library_dict[row[2]])
            cur.execute("insert or ignore into test_contents (center_name, contents_title, category, detail_link,"
                        "apply_start_date, apply_end_date, operate_start_date, operate_end_date,"
                        "edu_target,apply_target,max_apply_num,applied_num,wait_num,apply_state) values"
                        "(?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (row[2], element_str_list[tmp_row], 'none', detail_link,
                                                          row[4].split(" ~")[0], row[4].split(" ~")[1],
                                                          row[5].split(" ~")[0], row[5].split(" ~")[1],
                                                          row[6], row[7],
                                                          int(row[8].split("/")[0].split(":")[1].strip("명")),
                                                          int(row[8].split("/")[1].split(":")[1].split("명")[0]),
                                                          0, row[9])
                        )
        db.commit()
    db.close()

    return "finish initialize busan lib event"

@bp.route("/testdb/busan_event")
def busan_event():
    busan_event_url = "https://reserve.busan.go.kr/lctre/list?resveGroupSn=&progrmSn=&srchGugun=&srchResveInsttCd=&srchCtgry=&srchBeginDe=&srchEndDe=&srchVal=&srchList=Y"
    busan_event = pd.read_html(busan_event_url)
    busan_event = busan_event[0]
    db = get_db()
    for i in range(1,5):
        request_2 = requests.get(
            "https://reserve.busan.go.kr/lctre/list?curPage="+str(i)+"&resveGroupSn=&progrmSn=&srchGugun=&srchResveInsttCd=&srchCtgry=&srchBeginDe=&srchEndDe=&srchVal=&srchList=N"
            )
        soup_2 = bs(request_2.content, "html.parser")

        ids = soup_2.select('a.reserveItem')
        ids_list = []
        for id_ in ids:
            tmp_group = str(id_).split("fn_viewProgrm('")[1].split("')")[0].split("',")[0]
            tmp_prg = str(id_).split("fn_viewProgrm('")[1].split("')")[0].split(", '")[1]
            ids_list.append({'group': tmp_group, 'prg': tmp_prg})

        titles = soup_2.select("div.infoBox>p")
        title_list = []
        for title in titles:
            title_list.append(title.string)

        statuses = soup_2.select("div.infoBox>span.statusMark")
        status_list = []
        for status in statuses:
            status_list.append(status.string)

        dates = soup_2.select("dd.date>span")
        date_list = []
        for date in dates:
            date_list.append(date.string)

        date_dict = [{'신청': date_list[i].split("] ")[1], '행사': date_list[i + 1].split("] ")[1]} for i in
                     range(0, len(date_list), 2)]

        infos = soup_2.select("dd")
        info_list = []
        for info in infos:
            tmp = str(info).split('\t')[-1].split('</dd>')[0]
            if tmp[0] != '<':
                info_list.append(tmp.replace(u'\xa0', u''))

        info_dict = [{'기관': info_list[i], '대상': info_list[i + 1], '장소': info_list[i + 2], '문의': info_list[i + 3]} for i
                     in range(0, len(info_list), 4)]



        cur = db.cursor()

        for j in range(10):
            tmp_row=j+(10*i)
            detail_link = ('https://reserve.busan.go.kr/lctre/view?resveGroupSn='
            + ids_list[j]['group']+'&progrmSn='+ids_list[j]['prg']+'&srchGugun=&srchResveInsttCd=&srchCtgry=&srchBeginDe=&srchEndDe=&srchVal=')
            cur.execute("insert or ignore into test_contents (center_name, contents_title, category, detail_link,"
                        "apply_start_date, apply_end_date, operate_start_date, operate_end_date,"
                        "edu_target,apply_target,max_apply_num,applied_num,wait_num,apply_state) values"
                        "(?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (info_dict[j]['기관'], title_list[j], 'none', detail_link,
                                                          date_dict[j]['신청'].split(" ~")[0], date_dict[j]['신청'].split(" ~")[1],
                                                          date_dict[j]['행사'].split(" ~")[0], date_dict[j]['행사'].split(" ~")[1],
                                                          info_dict[j]['대상'], 'none',
                                                          int(busan_event.loc[tmp_row]['정원/접수/잔여'].split("/")[0].strip()),
                                                          int(busan_event.loc[tmp_row]['정원/접수/잔여'].split("/")[1].strip()),
                                                          0, status_list[j])
                        )
        db.commit()
    db.close()

    return "finish"

import pandas as pd

busan_lib_event_url = "https://home.pen.go.kr/yeyak/edu/lib/selectEduList.do?mi=14556&eduSeq=&srchRsSysId=&srchEduCtgry=&currPage=1&srchRsvSttus=&srchPeriodDiv=rcept&srchRsvBgnde=&srchRsvEndde=&srchRsvValue=&pageIndex=50"
busan_lib_event = pd.read_html(busan_lib_event_url)
busan_lib_event = busan_lib_event[0]
busan_lib_event

import requests
from bs4 import BeautifulSoup as bs
request = requests.get("https://home.pen.go.kr/yeyak/edu/lib/selectEduList.do?mi=14556&eduSeq=&srchRsSysId=&srchEduCtgry=&currPage=1&srchRsvSttus=&srchPeriodDiv=rcept&srchRsvBgnde=&srchRsvEndde=&srchRsvValue=&pageIndex=50")
soup = bs(request.content,"html.parser")
table=soup.findAll("a", class_="viewEduInfo")

libraries = soup.select("ul.tabList>li>a")[1:]
for library in libraries:
    tmp = str(library).split('data-id="')[1].split("\"")
    print(tmp[0], library.string)

elements=list(soup.select("a.viewEduInfo"))
for element in elements:
    tmp = str(element).split('class="')[1].split("\"")
    if tmp[0] == "viewEduInfo":
        print(tmp[4], element.string) #edu-se,data-id(edu-seq)

#url_base='https://home.pen.go.kr/yeyak/edu/lib/selectEduInfo.do?mi=14460&eduSeq='+{id}+'&srchRsSysId='+{library}







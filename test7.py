# -*- coding: utf-8 -*-


from bs4 import BeautifulSoup

import os

import datetime, time

from time import localtime, strftime

from datetime import timedelta

import urllib.request as urllib2

import xlwt



 

f = open("category.txt")

line = f.readline()

category_list = line.split('/')

f.close





#기간 산정하기

d = datetime.date.today()

 

#하루 기준으로 뽑기 

td = timedelta(days=3) # 3일치 뽑을거면 days 수정해주면 됨.

fromtd = d -td;

fromBidDt="20" + str(fromtd.strftime("%y/%m/%d"))

toBidDt = "20" + str(d.strftime("%y/%m/%d"))

 

#저장할 파일명 설명

doc_name = str(strftime("%y-%m-%d_%H%M%S", localtime()))







for category in category_list:

#excel 설정

    workbook = xlwt.Workbook(encoding='utf-8')

    workbook.default_style.font.heignt = 20*11   #font설정 11pt

     

    #사용자 정의 색깔 설정

    xlwt.add_palette_colour("lightgray", 0x21) 

    workbook.set_colour_RGB(0x21, 216, 216, 216)

    xlwt.add_palette_colour("lightgreen", 0x22) 

    workbook.set_colour_RGB(0x22, 216,228,188)

     

    #시트 생성 및 cell 가로 길이 설정

    worksheet = workbook.add_sheet(u'시트0')      

    col_width_0 = 256*13

    col_width_1 = 256*13

    col_width_2 = 256*21

    col_width_3 = 256*13

    col_width_4 = 256*13

    col_width_5 = 256*15

    col_width_6 = 256*16

    col_width_7 = 256*14

    col_width_8 = 256*13

    col_width_9 = 256*13

    col_width_10 = 256*23

     

    col_height_content = 48

     

    worksheet.col(0).width = col_width_0

    worksheet.col(1).width = col_width_1

    worksheet.col(2).width = col_width_2

    worksheet.col(3).width = col_width_3

    worksheet.col(4).width = col_width_4

    worksheet.col(5).width = col_width_5

    worksheet.col(6).width = col_width_6

    worksheet.col(7).width = col_width_7

    worksheet.col(8).width = col_width_8

    worksheet.col(9).width = col_width_9

    worksheet.col(10).width = col_width_10

     

    #폰트 스타일 생성

    #font_set = "font: name "+u"맑은 고딕" +", height 280;";

    #font_style = xlwt.easyxf(font_set)  

    #worksheet.row(0).set_style(font_style)         #줄에 폰트 스타일 설정

     

    # 항목 스타일 설정

    list_style = "font:height 180,bold on; pattern: pattern solid, fore_color lightgray; align: wrap on, vert centre, horiz center"

    #content_style_normal = "font:height 180; align:wrap on, vert centre"

    #content_style_center = "font:height 180; align:wrap on, vert centre, horiz center"

     

    # 엑셀에 항목 입력

    worksheet.write(0,0,u"Date", xlwt.easyxf(list_style))

    worksheet.write(0,1,u"업무", xlwt.easyxf("font:height 180, bold on;pattern: pattern solid, fore_color lightgreen; align:vert centre, horiz center"))

    worksheet.write(0,2,u"공고번호-차수", xlwt.easyxf(list_style))

    worksheet.write(0,3,u"분류", xlwt.easyxf(list_style))

    worksheet.write(0,4,u"공고명", xlwt.easyxf(list_style))

    worksheet.write(0,5,u"공고기관", xlwt.easyxf(list_style))

    worksheet.write(0,6,u"수요기관", xlwt.easyxf(list_style))

    worksheet.write(0,7,u"계약방법", xlwt.easyxf(list_style))

    worksheet.write(0,8,u"임력일시\n(마감일시)", xlwt.easyxf(list_style))

    worksheet.write(0,9,u"공동수급", xlwt.easyxf(list_style))

    worksheet.write(0,10,u"투찰", xlwt.easyxf(list_style))

    bidNm = category

    print ("[" + bidNm + "]검색중...")

    bidNm = urllib2.quote(category)

    instNm = ""

    radOrgan = 1

    fromOpenBidDt = "";

    toOpenBidDt = "";

    bidno="";

    urlString = "http://www.g2b.go.kr:8101/ep/tbid/tbidList.do?taskClCds=&bidNm=" + bidNm + "&searchDtType=1&fromBidDt=" + fromBidDt + "&toBidDt=" + toBidDt + "&fromOpenBidDt=" + fromOpenBidDt + "&toOpenBidDt=" + toOpenBidDt + "&radOrgan=" + str(radOrgan) + "&instNm="+instNm + "&area=&regYn=Y&bidSearchType=1&searchType=1"

    body = urllib2.urlopen(urlString)

    soup = BeautifulSoup(body)

    parse_tr = soup.find_all('table')[0]

    row_marker = 0

    column_marker = 0

    

    for row in parse_tr.find_all('tr'):

      column_marker = 0

      columns = row.find_all('td')

      

      for column in columns:

         tmpstr = column.get_text()

         string =  tmpstr

         worksheet.write(row_marker+1,column_marker+1,unicode(string))

         column_marker += 1

      if len(columns) > 0:

       row_marker += 1

  

    workbook.save(os.path.join(os.path.abspath("."), doc_name + category + u"_나라장터.xls"))
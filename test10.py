# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-

from gettext import Catalog
import os
import datetime, time
from time import localtime, strftime
from datetime import timedelta
import urllib.request as urllib2


# 나라장터에서 검색할 카테고리 txt 파일에서 가져오기 

f = open("category.txt")
line = f.readline()
category_list = line.split('/')
f.close

#### Field Description ####
#taskClCds = 업무구분
#bidNm = 공고명
#fromBidDt : 공고일 ~부터 2015%2F09%2F01
#toBidDt : 공고일 ~까지
#fromOpenBidDt=&toOpenBidDt= 개찰일 ~에서 ~까지
#instNm : 공공기관
#radOrgan : 1(공고기관) 2(수요기관)
#area : 지역
#bidno : 공고번호
#####################################

#기간 산정하기
d = datetime.date.today()


#하루 기준으로 뽑기 
td = timedelta(days=1) # 3일치 뽑을거면 days 수정해주면 됨.
fromtd = d -td;
fromBidDt="20" + str(fromtd.strftime("%y/%m/%d"))
toBidDt = "20" + str(d.strftime("%y/%m/%d"))
 
#저장할 파일명 설명
doc_name = str(strftime("%y-%m-%d_%H%M%S", localtime())) + "_나라장터.xls"


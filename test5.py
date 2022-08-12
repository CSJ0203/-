# In [0]:
import pandas as pd
import numpy as np
import requests
import os
import datetime, time
import string
from time import localtime, strftime
from datetime import timedelta
from tqdm import tqdm
from xlsxwriter.utility import xl_col_to_name, xl_range
from lxml import html
from subprocess import call

# In [1]:
#function to read txt files and parse the list
def txt_reader(name):
    a=[]
    f = open(name+".txt", mode='r', encoding='utf-8').readlines()
    for item in f:
        b = item.replace('\n','')
        a.append(b[:14])
    return a

# In [2]:
#load the categories with the txt_reader function
category_list = txt_reader('category')
print("category.txt에 저장된 키워드를 가져옵니다: " +str(category_list).replace('[','').replace(']','').replace("'",""))


# In [3]:
class KoreaPageScraper(object):
    def __init__(self):
        pass
    
    def request_url(self,cat):
        '''각 키워드 별 url을 가져옵니다. returns url for a  category'''
        #d는 오늘 날짜. end_date/toBidDt 값으로 사용합니다. 
        d = datetime.date.today()
        end_date =str(d.strftime("%Y/%m/%d"))
        toBidDt = requests.utils.quote(end_date, safe='')
        #fromtd로 일 주일 치 결과만을 가져옵니다. start_date/fromBidDt 값으로 사용합니다. 
        fromtd = d - timedelta(days=7)
        start_date = str(fromtd.strftime("%Y/%m/%d"))
        fromBidDt = requests.utils.quote(start_date, safe='')
        #키워드를 인코딩해 bidNm 값으로 사용합니다. 
        bidNm = requests.utils.quote(cat.encode('euc-kr'))
        #FYI: 검색어 뿐만 아니라 추가적인 parameter를 여기에다가 추가할 수도 있습니다. 
        #url = "http://www.g2b.go.kr:8101/ep/tbid/tbidList.do?taskClCds=&bidNm=" + bidNm + "&searchDtType=1&fromBidDt=" + fromBidDt + "&toBidDt=" + toBidDt + "&fromOpenBidDt=&toOpenBidDt=&radOrgan=1&instNm=&exceptEnd=Y&area=&regYn=Y&bidSearchType=1&searchType=1&recordCountPerPage=1000"
        url = "https://www.g2b.go.kr/pt/menu/selectSubFrame.do?framesrc=/pt/menu/frameTgong.do?url=https://www.g2b.go.kr:8101/ep/tbid/tbidList.do?taskClCds=&bidNm=" + bidNm + "&searchDtType=1&fromBidDt=" + fromBidDt + "&toBidDt=" + toBidDt + "&fromOpenBidDt=&toOpenBidDt=&radOrgan=1&instNm=&exceptEnd=Y&area=&regYn=Y&bidSearchType=1&searchType=1"
        return url

    def scrape_cat(self,cat):
        '''키워드를 검색합니다. searches for each category'''
        #위의 request_url function을 통해 생성된 url을 가봅니다. 
        cat_url = self.request_url(cat)
        #pandas의 read_html 기능을 이용해 테이블을 가져옵니다. 
        df = pd.read_html(cat_url)[0]
        #테이블에 'search_term'이라는 항목을 추가해 어떤 키워드로 검색해서 공고가 나왔는 지에 대한 정보를 추가합니다. 
        df['search_term']=cat
        return df
    
    def get_bidurl(self,bidnum):
        '''공고 상세페이지 url을 가져옵니다. gets the bid url based on the bid registration number 
        (ones that do not have a proper bid registration number usually doesn't have a corresponding link and would ask the user to go to the organization website for more informatioin)'''
        num_split = str(bidnum).split(sep='-')
        bidno = num_split[0]
        if len(bidno) == 11:
            bidseq = num_split[-1]
            bidurl = "http://www.g2b.go.kr:8081/ep/invitation/publish/bidInfoDtl.do?bidno="+bidno+"&bidseq="+bidseq
            return bidurl
        else: 
            return "Check organization website (공고기관) for details"
        bidseq = refnum_split[-1]
        bidurl = "http://www.g2b.go.kr:8081/ep/invitation/publish/bidInfoDtl.do?bidno="+bidno+"&bidseq="+bidseq
        return bidurl

    def scrape_categories(self, categories):
        '''각 키워드 별 리스트를 긁어옵니다. scrapes each keyword and compiles it into a list. 
        There is a 1 second delay between each search term to prevent getting blocked out of the site'''
        appended_df = []
        for category in tqdm(categories):
            one_df = self.scrape_cat(category)
            appended_df.append(one_df)
            time.sleep(1)
        appended_df = pd.concat(appended_df, axis = 0)
        urlist=[]
        for index,row in appended_df.iterrows():
            urlist.append(self.get_bidurl(row['공고번호-차수']))
            
        appended_df['url']=urlist
        return appended_df
    
# In [4]:
#scrape with the "KoreaPageScraper" class
myscraper = KoreaPageScraper()

df = myscraper.scrape_categories(category_list)


# In [5]:
print(str(len(df))+"개의 공고를 찾았습니다. ")

# In [6]:
#Load the excluding keywords
excluding=txt_reader('exclude')
print("exclude.txt에서 제외할 키워드를 가져옵니다: "+str(excluding).replace('[','').replace(']','').replace("'",""))


# In [7]:
contains_excluding = str(excluding).replace('[','').replace(']','').replace("'","").replace(", ","|")


# In [8]:
#Deleting the excluding keywords and informing how many lines were deleted. 
og = len(df)
df = df[-df.공고명.str.contains(contains_excluding).fillna(True)]
print(str(og-len(df))+"개의 공고를 제외하였음. (현재 "+str(len(df))+"개의 공고가 남아있음)")


# In [9]:
def clean_up(df):
    #Delete duplicates (more than two keywords together)
    og2 = len(df)
    df = df[~df.duplicated(['공고명'])].copy()
    print(str(og2-len(df))+"개의 중복 항목이 발견되어 삭제하였습니다. (현재 "+str(len(df))+"개의 공고가 남아있음)")
    #Divide the register date and due date
    df['register_date'],df['duedate'] = df['입력일시(입찰마감일시)'].str.split('(', 1).str
    df['duedate']=df['duedate'].str.replace(')','').replace('-','')
    df = df.drop('입력일시(입찰마감일시)',axis=1)
    #Sort the values by duedate. To sort with a different value, change the following line's 'duedate' with the column name you desire to sort it by. 
    column_sort = 'duedate'
    df = df.sort_values(by=column_sort,ascending=False)
    print("현재 공고 나열 순서는 '"+column_sort+"' 항목 내림차순입니다. 이를 바꾸기 위해서는 툴 관리자에게 연락 바랍니다. ")
    return df

# In [10]:
#Cleaning up the df to make more sense
clean_df = clean_up(df)


# In [11]:
#Adding the price information
class AdditionalInfo(object):
    def __init__(self):
        pass
    
    def get_tree(self,page):
        r=requests.get(page)
        tree = html.fromstring(r.content)
        return tree

    def ext_link(self,page):
        tree = self.get_tree(page)
        file_link = tree.xpath('//*[@id="container"]/div[17]/table/tbody/tr[*]/td[3]/div/a')
        linklist = []
        for links in file_link:
            a = links.values()[0]
            b = a[a.find("(")+1:].split(',')[0].replace("'",'')
            c = "http://www.g2b.go.kr:8081/ep/co/fileDownload.do?fileTask=NOTIFY&fileSeq="+b
            linklist.append(c)
        return linklist

    def price(self,page):
        tree = self.get_tree(page)
        table_ptag = None
        for l in tree.xpath('//*[@class="section"]/p'):
            if l.text.startswith('예정가격'):
                table_ptag = l
                break

        x=table_ptag.getparent()
        budget_table = pd.read_html(html.tostring(x))[0]
        baejung = budget_table[1][1]
        baejung = int(baejung[:baejung.find('원')].replace(",","").replace("￦",""))
        return baejung
    
    
#In [12]:
x = AdditionalInfo()
print("가격 정보를 가져옵니다:")
test_list = []
for index,row in tqdm(clean_df.iterrows(), total=len(clean_df)):
    try:
        p = x.price(row.url)
    except:
        p = None
    test_list.append(p)

clean_df['budget'] = test_list


# In [13]:
class create_excel(object):
    def get_length(self,column):
        valueex = column[~column.isnull()].reset_index(drop=True)[0]
        if type(valueex) == str:
            len_list = list(column.dropna().apply(lambda x: len(str(x))))
            maxlen = max(len_list)
            medlen = np.median(len_list)
            meanlen = np.mean(len_list)
            diff = maxlen-medlen
            stdlen = np.std(len_list)
            #min(A,B+C*numchars)
            if maxlen < 10:
                return maxlen+5
            elif diff > 50:
                if medlen == 0:
                    return min(55,meanlen+5)
                return medlen
            elif maxlen < 50:
                return meanlen+15
            else:
                return 50
        else:
            return 5

    def to_excel(self,df,name):
        #Next step, format the excel file
        print("saving the "+name+" list...")
        docname = "나라장터_입찰공고-"+name+"-"+str(strftime("%y%m%d(%H%M%S)", localtime()))+".xlsx"
        #make the destination directory, but guard against race condition
        if not os.path.exists(name):
            try:
                os.makedirs(name)
            except OSError as exc: 
                print(exc)
                raise Exception('something failed')
        writer = pd.ExcelWriter("%s/%s"%(name,docname), engine='xlsxwriter')
        df.to_excel(writer,index=False,sheet_name='Sheet1')
        workbook  = writer.book
        worksheet = writer.sheets['Sheet1']
        tablerange = xl_range(0,0,len(df),len(df.columns)-1)
        headerrange = xl_range(0,0,0,len(df.columns)-1)
        contentrange = xl_range(1,0,len(df),len(df.columns)-1)

        #Formatting headers
        header_format = workbook.add_format({'bg_color':'black'})
        column_format = workbook.add_format({'bottom':True,'bg_color':'white'})
        link_format = workbook.add_format({'font_color':'#157993','underline':True})
        
        # Set the column width and format.
        columns = []
        widths = []
        for i in range(0,len(df.columns)):
            a = xl_col_to_name(i)+":"+xl_col_to_name(i)
            columns.append(a)
            widths.append(self.get_length(df[df.columns[i]])) 
        
        for c,w in zip(columns,widths):
            worksheet.set_column(c, w)
        
        worksheet.conditional_format(contentrange,{'type':'no_errors',
                                                   'format':column_format})
        worksheet.conditional_format(headerrange,{'type':'no_errors',
                                                  'format':header_format})
        worksheet.conditional_format(tablerange,{'type':'text',
                                                 'criteria':'containing',
                                                 'value':'Click link',
                                                 'format':link_format})
           
        #Formatting for putting in the header titles
        table_headers = [{'header':c} for c in  df.columns]
        #Create a table with the data
        worksheet.add_table(tablerange,{'columns' : table_headers})         
        
        writer.save()
        return
    
#In [14]:
go_to_excel = create_excel()


#In [15]:
go_to_excel.to_excel(clean_df,'full')

# In [16]:
print ('All done! Please hit Enter to exit this command prompt. ')
input()


#In [17]:
call(['explorer','full'])

#In [18]:

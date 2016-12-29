#-*- coding: UTF-8 -*-
import json
import requests
from BeautifulSoup import BeautifulSoup as bs4

# initial request paraments
s = requests.session()
header = {'Content-Type': 'application/json; charset=UTF-8'}
courseList = {}

def init():
    url = "http://service002.sds.fcu.edu.tw/main.aspx?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE0ODIwODY2MTN9.zRhVTM5MHdVFuZFbvFW4gwrm3sTg_33EyTZECZ22DrM"
    r = s.get(url)

def getContents(api):
    global courseList
    url = "http://140.134.20.80/W320104/action/getdata.aspx/getCourseInfo"
    header2 = {'Origin": "http://140.134.20.80' ,
                'Accept-Encoding": "gzip, deflate' ,
                'Accept-Language": "zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4' ,
                'User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36' ,
                'Content-Type": "application/json; charset=UTF-8' ,
                'Accept": "application/json, text/plain, */*' ,
                'Referer": "http://140.134.20.80/W320104/index.htm?20161214v2' ,
                'Cookie": "ASP.NET_SessionId=rt51ev45hc305d45ovw5f345' ,
                'Connection": "keep-alive'}
    data = {"course_id":"69cb393483566c4b96bbeff1916a72e89b5c03ccc50bf4899ecd1669b4ee57d2107fcbbfdb066737"}
    r = s.post(url,headers=header2,json=data);
    return r
    result = json.loads(json.loads(r.text)['d'])
    print result
    #print "Week " + str(week) + ", Period = " + str(period) + " crawled"
    pass

# get Course Lists
def getType2Result():
    global courseList
    year = 105
    semester = 1
    url = "http://service002.sds.fcu.edu.tw/Service/Search.asmx/GetType2Result"
    for week in range(1,8):
        for period in range(15):
            data = {"baseOptions":{"lang":"cht","year":year,"sms":semester},
                    "typeOptions":{
                        "code":{"enabled":False,"value":""},
                        "weekPeriod":{"enabled":True,"week":week,"period":period},
                        "course":{"enabled":False,"value":""},
                        "teacher":{"enabled":False,"value":""},
                        "useEnglish":{"enabled":False},
                        "specificSubject":{"enabled":False,"value":"1"}}
                    }
            r = s.post(url,headers=header,json=data);
            courses = json.loads(json.loads(r.text)['d'])['items']
            for course in courses:
                courseID = "1052" + course['cls_id'] + course['sub_id'] + course['scr_dup']
                course['year'] = year
                course['semester'] = semester
                courseList[courseID] = course 
            print "Week " + str(week) + ", Period = " + str(period) + " crawled"

init()
getType2Result()
i = 1
count = 0
temp = {}
for items in courseList:
    temp[items] = courseList[items]
    count += 1
    if count % 100 == 0:
        open("1051/CourseList"+str(i)+".json","w").write(json.dumps(temp).encode('utf-8'))
        i += 1
        temp = {}
#r = getContents("getCourseInfo")


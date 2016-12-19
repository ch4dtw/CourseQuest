#-*- coding: UTF-8 -*-
import json
import requests
from BeautifulSoup import BeautifulSoup as bs4
dicts = []

# initial request paraments
s = requests.session()

def init():
    url = "http://service002.sds.fcu.edu.tw/main.aspx?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE0ODIwODY2MTN9.zRhVTM5MHdVFuZFbvFW4gwrm3sTg_33EyTZECZ22DrM"
    r = s.get(url)

# get Department Lists
def getDeptList():
    global dicts
    open("DepartmentList.txt","w").write('')
    degree = ['??','大學部','??','碩士班','博士班','進修學士班']
    url = "http://service002.sds.fcu.edu.tw/Service/Search.asmx/GetDeptList"
    header = {
        'Content-Type': 'application/json; charset=UTF-8'
    }
    # Six Degree
    for i in range(6):
        data = {
            "baseOptions":{"lang":"cht","year":105,"sms":2},"degree":i
        }    
        r = s.post(url,headers=header,json=data);
        content = "// " + degree[i] + "\n" + r.text.encode('utf-8') + '\n'
        open("DepartmentList.txt","a").write(content)
        dicts.append(json.loads(r.text))
    
# get Department Lists
def getUnitList():
    pass
init()
getDeptList()

open("UnitList.txt","w").write('')
degree = ['??','大學部','??','碩士班','博士班','進修學士班']
url = "http://service002.sds.fcu.edu.tw/Service/Search.asmx/GetUnitList"
header = {
    'Content-Type': 'application/json; charset=UTF-8'
}
# Six Degree
#for i in range(6):
for dept in range(5):
    data = {"baseOptions":{"lang":"cht","year":105,"sms":2},"degree":"1","deptId":dept}
    r = s.post(url,headers=header,json=data);
    content = "// " + degree[dept] + "\n" + r.text.encode('utf-8') + '\n'
    open("DepartmentList.txt","a").write(content)
    


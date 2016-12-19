#-*- coding: UTF-8 -*-
import json
import requests
from BeautifulSoup import BeautifulSoup as bs4

# initial request paraments
s = requests.session()
header = {'Content-Type': 'application/json; charset=UTF-8'}
degrees = ['??','大學部','??','碩士班','博士班','進修學士班']
departments = {}
units = {}

def init():
    url = "http://service002.sds.fcu.edu.tw/main.aspx?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE0ODIwODY2MTN9.zRhVTM5MHdVFuZFbvFW4gwrm3sTg_33EyTZECZ22DrM"
    r = s.get(url)

# get Department Lists
def getDeptList():
    #global departments,header,degree
    open("DepartmentList.txt","w").write('')
    url = "http://service002.sds.fcu.edu.tw/Service/Search.asmx/GetDeptList"
    # Six Degree
    for degree in range(6):
        data = {"baseOptions":{"lang":"cht","year":105,"sms":2},"degree":degree}    
        r = s.post(url,headers=header,json=data);
        content = "// " + degrees[degree] + "\n" + r.text.encode('utf-8') + '\n'
        open("DepartmentList.txt","a").write(content)
        departments[degree] = json.loads(r.text)
        print degrees[degree] + " crawled"
    
# get Department Lists
def getUnitList():
    #global departments,degree,header
    open("UnitList.txt","w").write('')
    url = "http://service002.sds.fcu.edu.tw/Service/Search.asmx/GetUnitList"
    # Six Degree
    for degree in departments:
        depts = json.loads(departments[degree]['d'])
        units[degree] = depts 
        j = 0
        for dept in depts:
            print dept['name'].encode('utf-8') + " crawed"
            data = {"baseOptions":{"lang":"cht","year":105,"sms":2},"degree":degree,"deptId":dept['id']}
            r = s.post(url,headers=header,json=data);
            content = "// " + degrees[degree] + " " + dept['name'].encode('utf-8') + "\n" + r.text.encode('utf-8') + '\n'
            open("UnitList.txt","a").write(content)
            units[degree][j]['unit'] = json.loads(json.loads(r.text)['d'])
            j = j+1

# get Department Lists
def getClassList():
    #global dicts,degree,header
    open("ClassList.txt","w").write('')
    url = "http://service004.sds.fcu.edu.tw/Service/Search.asmx/GetClassList"
    # Six Degree
    for degree in units:
        for depts in units[degree]:
            for unit in depts['unit']:
                print unit['name'].encode('utf-8') + " crawed"
                data = {"baseOptions":{"lang":"cht","year":105,"sms":2},"degree":degree,"unitId":unit['id']}
                r = s.post(url,headers=header,json=data);
                content = "// " + degrees[degree] + " " + depts['name'].encode('utf-8') + " " + unit['name'].encode('utf-8') + "\n" + r.text.encode('utf-8') + "\n"
                open("ClassList.txt","a").write(content)

init()
getDeptList()
getUnitList()
getClassList()
    

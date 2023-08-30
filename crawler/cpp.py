import json
import os
import time

import certifi
import requests
class CppCrawler:
    def __init__(self):
        # self.net_websocket=''
        # self.getsocket_url='https://ws.allcpp.cn/socket.io/?EIO=3&transport=polling'
        # self.setwebsocket_url=""
        self.data={}
        self.token_data = {}
        self.session = requests.session()
        self.ticket = {}
        self.ticketlist = []
        self.personMai = []
        self.personlist = []
        self.manzhanlist = []
        self.manzhan = {}
        self.version = ""
        self.account = ""
        self.password = ""
        self.read_json()
        self.timesleep=1
        if self.timesleep==1:
            self.timesleep=eval(input("请输入抢票间隔："))
        if bool(self.data):
            if 'ticket' in self.data:
                self.ticket = self.data["ticket"]
            if 'ticketlist' in self.data:
                self.ticketlist = self.data["ticketlist"]
            if 'personMai' in self.data:
                self.personMai = self.data["personMai"]
            if 'personlist' in self.data:
                self.personlist = self.data["personlist"]
            if 'manzhan' in self.data:
                self.manzhan = self.data["manzhan"]
            if 'version' in self.data:
                self.version = self.data["version"]
            if 'account' in self.data:
                self.account = self.data["account"]
            if 'password' in self.data:
                self.password = self.data["password"]
        if self.account=="":
            self.account=input("请输入账号:")
            self.write_json("account",self.account)
        if self.password=="":
            self.password=input("请输入密码:")
            self.write_json("password", self.password)
        if self.version=="":
            self.version=input("请输入当前app版本:")
            self.write_json("version", self.version)

    # def getwebSocketToken(self):
    #     """
    #     获取建立websocket链接的token
    #     :return:
    #     """
    #     header={
    #         "user-agent":"okhttp/3.7",
    #     }
    #     result=requests.get(self.getsocket_url,header)
    #     match=re.search(r"\{(.+)\}",result.text)
    #     if match:
    #         jsonstr=match.group(0)
    #         data=json.loads(jsonstr)
    #         print(data)
    #         self.token_data=data
    # def setWebsocket(self,data:dict):
    #     self.setwebsocket_url=f"https://ws.allcpp.cn/socket.io/?EIO=3&sid={data.get('sid')}&transport=polling"
    #     header={
    #         "user-agent":"okhttp/3.7",
    #     }
    #     print(self.setwebsocket_url)
    #     while True:
    #         result=requests.get(self.setwebsocket_url,header)
    #         print(result.text)
    #         time.sleep(int(data["pingInterval"])/1000)

    def startLogin(self):
        url="https://user.allcpp.cn/api/login/normal"
        header={
            "User-Agent":"okhttp/3.14.7",
            "Origin":"https://cp.allcpp.cn",
            "Referer":"https://cp.allcpp.cn",
            "content-type":"application/x-www-form-urlencoded",
            "appheader":"mobile",
            "equipmenttype":"1",
            "deviceversion":"25",
            "devicespec":"SM-G9810",
            "appversion":self.version
        }
        params={
            "account":self.account,
            "password":self.password,
            "deviceId":"b615637e514d53564a6b6f9da1b94c51",
            "bid":"cn.comicup.apps.cppub",
            "equipmenttype": 1,
            "deviceversion": 25,
            "devicespec": "SM-G9810",
            "token":""
        }
        result=self.session.post(url,headers=header,verify=certifi.where(),params=params)
        print(result.text)
        data=self.session.cookies.get_dict()
        #{'token': 'hX+4bfsJgbs4cPl+SMu3yqSd9kU1E+V20FRK7Jr3JDcG/GFVRELfCYce+0O8p6ZZdbax4vs2FH+yQujcH9hGbJ0e1WTZUsWdVhtZfqsikxkMYk/Biv5g9ibjeLfDN9smDI9R+MD6VegLqMzO8VCcHEJkmu4IjgCFDRH2sn0TeAE=', 'JSESSIONID': 'D52CE5B1D7226DB00C2F560256C4BB73'}
        print(self.session.cookies.get_dict())
        return data
    def getPiaoJia(self):
        cookie=self.session.cookies.get_dict()
        eventid=self.manzhan.get("eventMainId")
        header = {
            "User-Agent": "okhttp/3.14.7",
            "Origin": "https://cp.allcpp.cn",
            "Referer": "https://cp.allcpp.cn",
            "content-type": "application/x-www-form-urlencoded",
            "appheader": "mobile",
            "equipmenttype": "1",
            "deviceversion": "25",
            "devicespec": "SM-G9810",
            "appversion": self.version
        }
        params = {
            "eventMainId":eventid,
            "ticketMainId":"0",
            "deviceId": "b615637e514d53564a6b6f9da1b94c51",
            "bid": "cn.comicup.apps.cppub",
            "equipmenttype": 1,
            "deviceversion": 25,
            "devicespec": "SM-G9810",
            "token": cookie.get('token')
        }
        url=f"https://www.allcpp.cn/allcpp/ticket/getTicketTypeList.do"
        result=self.session.get(url,headers=header,params=params,verify=certifi.where())
        resultjson :dict =json.loads(result.text)
        ticketList=resultjson.get("ticketTypeList")
        self.ticketlist=ticketList
        self.write_json("ticketlist", self.ticketlist)
        pass
    def chosePiao(self):
        ticketList=self.ticketlist
        for i in range(len(ticketList)):
            ticket=ticketList[i]
            print(str(i)+"."+str(ticket["ticketName"])+"---"+str(int(ticket["ticketPrice"])/100))
        a=input("请输入购票序号：")
        a=int(a)
        self.ticket=ticketList[a]
        self.write_json("ticket", self.ticket)
    def createOrder(self):
        url="https://www.allcpp.cn/api/ticket/buyticketalipay.do"
        cookie=self.session.cookies.get_dict()
        ticket=self.ticket
        header = {
            "User-Agent": "okhttp/3.14.7",
            "Origin": "https://cp.allcpp.cn",
            "Referer": "https://cp.allcpp.cn",
            "content-type": "application/x-www-form-urlencoded",
            "appheader": "mobile",
            "equipmenttype": "1",
            "deviceversion": "25",
            "devicespec": "SM-G9810",
            "appversion": self.version
        }
        params = {
            "count": 1,
            "purchaserIds":str(self.personMai[0]),
            "ticketTypeId": ticket.get("id"),
            "deviceId": "b615637e514d53564a6b6f9da1b94c51",
            "bid": "cn.comicup.apps.cppub",
            "equipmenttype": 1,
            "deviceversion": 25,
            "devicespec": "SM-G9810",
            "token": cookie.get('token')
        }
        result=self.session.post(url,headers=header,params=params,verify=certifi.where())
        return json.loads(result.text)
    def getGouPiaoRenInfo(self):
        url="https://www.allcpp.cn/allcpp/user/purchaser/getList.do"
        cookie=self.session.cookies.get_dict()
        header = {
            "User-Agent": "okhttp/3.14.7",
            "Origin": "https://cp.allcpp.cn",
            "Referer": "https://cp.allcpp.cn",
            "content-type": "application/x-www-form-urlencoded",
            "appheader": "mobile",
            "equipmenttype": "1",
            "deviceversion": "25",
            "devicespec": "SM-G9810",
            "appversion": self.version
        }
        params={
            "deviceId": "b615637e514d53564a6b6f9da1b94c51",
            "bid": "cn.comicup.apps.cppub",
            "equipmenttype": 1,
            "deviceversion": 25,
            "devicespec": "SM-G9810",
            "token": cookie.get('token')
        }
        result=self.session.get(url,headers=header,params=params,verify=certifi.where())
        resultjson=json.loads(result.text)
        self.personlist=resultjson
        self.write_json("personlist", self.personlist)
        print(resultjson)
    def searchManzhanInfo(self):
        a=input("请输入关键字:")
        cookie = self.session.cookies.get_dict()
        url="https://www.allcpp.cn/api/event/getEventMainList.do"
        header = {
            "User-Agent": "okhttp/3.14.7",
            "Origin": "https://cp.allcpp.cn",
            "Referer": "https://cp.allcpp.cn",
            "content-type": "application/x-www-form-urlencoded",
            "appheader": "mobile",
            "equipmenttype": "1",
            "deviceversion": "25",
            "devicespec": "SM-G9810",
            "appversion": self.version
        }
        params = {
            "cityid":0,
            "isnew":1,
            "orderbyid":1,
            "searchstring":a,
            "typeid":0,
            "pageSize":20,
            "pageindex":1,
            "deviceId": "b615637e514d53564a6b6f9da1b94c51",
            "bid": "cn.comicup.apps.cppub",
            "equipmenttype": 1,
            "deviceversion": 25,
            "devicespec": "SM-G9810",
            "token": cookie.get('token')
        }
        result=self.session.post(url,headers=header,params=params,verify=certifi.where())
        resultjson = json.loads(result.text)
        self.manzhanlist=resultjson["result"]["list"]
        for i in range(len(self.manzhanlist)):
            print(str(i)+"---"+str(self.manzhanlist[i]["eventName"]))
        if len(self.manzhanlist)==0:
            self.searchManzhanInfo()
        else:
            a = input("请输入漫展信息序号：")
            self.manzhan = self.manzhanlist[int(a)]
            self.write_json("manzhan", self.manzhan)
        return resultjson
    def qiangQiao(self):
        isSucc=False
        while not isSucc:
            resultjson=self.createOrder()
            print(resultjson)
            isSucc=resultjson["isSuccess"]
            if isSucc:
                print("抢到票啦，请及时付款")
                break
            time.sleep(self.timesleep)
    def choseGoupiaoren(self):
        for i in range(len(self.personlist)):
            print(str(i)+"--"+str(self.personlist[i]["realname"])+"--"+str(self.personlist[i]["mobile"]))
        a=input("请选择购票人序号(大于当前索引即可退出)：")
        while int(a)<=i:
            self.personMai.append(self.personlist[int(a)]["id"])
            a = input("请选择购票人序号：")
        print("选择成功")
        self.write_json("personMai",self.personMai)
    def read_json(self):
        if os.path.exists('cpp.json'):
            with open('cpp.json', 'r', encoding='gbk') as fp:
                self.data = json.load(fp)
            fp.close()
        else:
            with open('cpp.json', 'w', encoding='gbk') as fp:
                json.dump(self.data, fp, ensure_ascii=False)
            fp.close

    def write_json(self,key,value):
        self.data[key]=value
        with open('cpp.json', 'w', encoding='gbk') as fp:
            json.dump(self.data, fp, ensure_ascii=False)
        fp.close














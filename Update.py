# 線上更新也能使用，只是免費空間會自動還原環境，必須採用手動更新
def UpdateMain(message):
    if message.find("更新") == 0:
        print("需要一段時間，請稍後......更新完成另發通知")
        # UpdMsg = UpdatePTTBeauty(0)
        FlowerMain(message)
        print("更新完成")
    elif message == "檢查":
        contents = Parameter()
        s = '\n'.join(v + "=" + str(contents[v]) for v in contents)
        print(s)
    elif message == "重複":
        Message = []
        Message.append(DelRepeat("Flower", "Flower.txt"))
        Message.append(DelRepeat("PTTBeauty", "B.txt"))
        print(Message)
    print("UpdateMain")
    L = {}
    L["MessageLog"] = datetime.datetime.now().strftime("%Y/%m/%d %H:%M") + " Message " + message
    WriteParameter(L)
# region Update Pic DataBase
from bs4 import BeautifulSoup
import requests
import time
import datetime
import codecs
import json

# region Public Function
# MyStr = a,b,c,d,e,f => {'a':'b','c':'d','e':'f'}
def Str2Dict(MyStr,SpChar="_"):
    # print("MyStr",MyStr)
    lst_str = MyStr.split(SpChar)
    it = iter(lst_str)
    return dict(zip(it, it))
def GetRequest(Url):
    # print("Please Wait 1 Second")
    time.sleep(2)
    req = requests.get(url=Url, headers={'Content-type': 'text/plain; charset=utf-8'}, timeout=10)
    try:
        if (req.headers["Content-Type"].find("charset=Big5") > 0):
            result = req.content.decode("big5")
        else:
            result = req.content.decode("utf8")
    except:
        result = ""

    return result
def intTry(Val=None):
    try:
        if Val == "":
            return 1
        return int(Val)
    except:
        return 0
def Parameter():
    with codecs.open("Parameter.txt", "r","utf8") as file:
        s = file.read().replace("\n", "=")
        return Str2Dict(s, "=")
def WriteParameter(contents):
    print("Logs contents=", contents)
    s = '\n'.join(v + "=" + str(contents[v]) for v in contents)
    print("Logs s=", s)
    with codecs.open("Parameter.txt", "a","utf8") as wfile:
        wfile.write(s + "\n")
def Log(Type, AddPicNum):
    print("Log Function")
    d = Parameter()
    NewD = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")
    # Send Message
    if list(d.keys()).count('Update') is 0:
        d['Update'] = "None"
    msg = "Update Date : " + d['Update'] + "->" + NewD
    msg = msg + "\n" + "Add " + str(AddPicNum) + " Picture"

    filePath = "Flower.txt" if Type == "Flower" else "B.txt"
    with open(filePath, "r") as file:
        TotalPic = len(file.read().split("\n"))
    NewUpd = {}
    print("[" + Type + "]_" + NewD + " Total " + str(TotalPic) + " Insert " + str(AddPicNum))
    NewUpd['Update'] = "[" + Type + "]_" + NewD + " Total " + str(TotalPic) + " Insert " + str(AddPicNum)

    WriteParameter(NewUpd)
    return msg
def DelRepeat(Type, filename):
    with open(filename,"r") as r:
        data = r.read().split("\n")
    Org = len(data)
    data = list(set(data))
    New = len(data)
    with open(filename, "w") as w:
        w.writelines(list(row.replace("\n","")+"\n" for row in data))
    return "After Repeat Function \n [" + Type + ".txt] TotalPic=" + str(Org) + "->" + str(New)
# endregion

# region Update PTT Beauty
def WriteData(Type,l):
    print("-----write down img-" + str(len(l)) + "-----")
    filePath = "Flower.txt" if Type == "Flower" else "B.txt"
    if(Type == "Flower"):
        l = list(row.replace("\n", "") + "\n" for row in l)
    else:
        l = list(row.replace("\n", "") + ".jpg\n" for row in l)

    with codecs.open(filePath, "a", "utf8") as f:
        f.writelines(l)
def UpdatePTTBeauty(PageNum):
    prePage = ""
    UHeader = "https://www.ptt.cc"
    url = UHeader+"/bbs/Beauty/index.html"
    N = 0
    AddPicNum = 0

    # region Handle
    while N <= PageNum:
        N = N + 1
        time.sleep(2)
        print("Now Number = ", N)

        # region Paging
        if prePage is not "":
            url = prePage
        print("Now Url = ", url)
        html = GetRequest(url)
        soup = BeautifulSoup(html, 'html.parser')
        Paging = soup.find('div', {'class': 'btn-group-paging'})
        prePage = UHeader + Paging.select('a')[1].get('href')
        print("Next Url = ", prePage)
        # endregion

        # region subUrl
        subUrl = []
        title = soup.findAll('div', {'class': 'title'})
        for t in title[:2]:
            if str(t).find("<a href") >= 0:
                tObj = t.find_all("a")[0]
                subUrl.append(UHeader+tObj.get("href"))
                # print(tObj.text)
        # endregion

        # region UpdatePic
        for su in subUrl:
            l = SearchPicUrl(su)
            print("PicNum : ",len(l))
            AddPicNum = AddPicNum + len(l)
            WriteData(l)
        # endregion
    # endregion

    msg = Log(AddPicNum)

    return msg
def SearchPicUrl(url):
    print(url)
    html = GetRequest(url)
    soup = BeautifulSoup(html, 'html.parser')
    t = []
    for p in soup.findAll('div', {'class': 'richcontent'}):
        imgObj = p.find('a')
        if imgObj is not None:
            t.append(imgObj.get('href').replace("//","https://")+"\n")
    return t
# endregion

# region Update Flower
def FlowerMain(message):
    # message = "更新-19403052-3"
    if(message.count("-") != 2):
        print("Example : 更新-19403052-3")
        return False

    lst = message.split('-')
    boardsID = lst[1]
    totalN = lst[2]
    print(boardsID, totalN)

    # boardsID = "19403052"
    # totalN = 2
    Url = "https://huaban.com/boards/" + boardsID + "/"
    for i in range(int(totalN)):
        print("Loop",i+1,"/",totalN)
        time.sleep(1)
        NextUrl = GetFlowerImg(Url)
        Url = NextUrl
def FlowWriteFile(lstPins):
    t = []
    for row in lstPins:
        subUrl = "https://hbimg.huabanimg.com/"+row["file"]["key"]
        t.append(subUrl)

    WriteData("Flower",t)
    Log("Flower",len(t))
    # url = "https://huaban.com/boards/19403052/?jv3wp3bb&max=2413593581&limit=20&wfl=1"
    lastPins = lstPins[len(lstPins) - 1]
    lastPin_id = lastPins["pin_id"]
    boardID = lastPins["board_id"]
    NextUrl = "https://huaban.com/boards/" + str(boardID) + "/?jv3wp3bb&max=" + str(lastPin_id) + "&limit=20&wfl=1"
    print("NextUrl=",NextUrl)
    return NextUrl
def GetFlowerImg(url):
    d = GetRequest(url)
    content = ""
    for row in d.split('\n'):
        if row.find('"board"') > 0:
            content = row

    j = json.loads(content.replace('app.page["board"] = ', "")[:-1])
    user_id = j["user_id"]
    board_id = j["board_id"]
    return FlowWriteFile(j["pins"])
# endregion
# endregion
# endregion

# region For This Update.py
def LineMessageResponse(Msg):
    if(type(Msg) == "list"):
        for m in Msg:
            print(m)
    else:
        print(Msg)
# endregion

if __name__ == "__main__":
    # 更新-boardID-迴圈次數(1次約20張)  更新-24116838-30  更新-52334297-30 19403052
    # l = ["更新-24116838-40","更新-52334297-40","更新-19403052-40"]
    # for m in l:
    RequestMessage = input("像LineBot一樣的輸入(更新、檢查、重複)，更新請比照格式 : ")
    UpdateMain(RequestMessage)
    # t = Parameter()
    # print(t["MessageLog"])

# encoding: utf-8
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

app = Flask(__name__)

# 填入你的 message api 資訊
Token = "hR+zZ1KpsaRQYcF9CIvvsc4rVvZ1tHaQgjz1JlBOIvLLtMW7n6yaSHqhksoJtqWKw7iOBSoO6bKpIxJbk/VPAW/+ROcRTU5L5kYEiX8WhJhSWqU1YFhQkK0knhTkVSd3LlHDZ2C/LMi6GW8GU7U2PwdB04t89/1O/w1cDnyilFU="
channel = "69df63f9a6f70870fc131c5d6045d4a9"
# userID = "Ua1f0d71da0aa5d12d0132aba8cff150f"

line_bot_api = LineBotApi(Token)
handler = WebhookHandler(channel)

# 設定你接收訊息的網址，如 https://YOURAPP.herokuapp.com/callback
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print("Request body: " + body, "Signature: " + signature)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("Handle: reply_token: " + event.reply_token + ", message: " + event.message.text)
    # content = "{}: {}".format(event.source.user_id, event.message.text)
    if event.message.text == "更新":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="需要一段時間，請稍後......更新完成另發通知1"))
        UpdMsg = UpdateCrawlerMain(0)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=UpdMsg))

    elif event.message.text == "檢查":
        contents = Parameter()
        s = '\n'.join(v + "=" + str(contents[v]) for v in contents)
        print(s)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=s))
    else:
        if str(event.message.text).find("抽") != -1: # 是否含有"抽"
            FilterMsg = str(event.message.text).replace("抽","")  # 取代後的訊息
            Num = intTry(FilterMsg) # 取代後訊息是否能轉換成數值
            print(Num, "次")
            line_bot_api.reply_message(
                event.reply_token,
                returnContent(event.message.text,Num))


import os
import random
def returnContent(U_Receive,Times):
    # C = TextSendMessage(text=U_Receive)
    if str(U_Receive).find("抽") != -1:
        if Times <= 5:
            lst = []
            for i in range(Times):
                img = RandomPic()
                C = ImageSendMessage(
                    # type='image',
                    original_content_url=img,  # Pic Url
                    preview_image_url=img  # Preview Pic
                )
                lst.append(C)
                print(img, i,"/",Times, "次")
            return lst

def RandomPic():
    img = "https://m1.ablwang.com/uploadfile/2017/0901/20170901042508280.jpg"
    with open("B.txt","r") as file:
        d = file.read()
        l = d.split("\n")
        img = random.choice(l)
    return img

# region Update Pic DataBase
from bs4 import BeautifulSoup
import requests
import time
import datetime
import codecs

# region Public Function
# MyStr = a,b,c,d,e,f => {'a':'b','c':'d','e':'f'}
def Str2Dict(MyStr,SpChar="_"):
    # print("MyStr",MyStr)
    lst_str = MyStr.split(SpChar)
    it = iter(lst_str)
    return dict(zip(it, it))
def GetRequest(Url):
    # print("Please Wait 1 Second")
    time.sleep(1)
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
# endregion

def Parameter():
    with open("Parameter.txt","r") as file:
        s = file.read().replace("\n", "=")
        return Str2Dict(s, "=")

def WriteParameter(contents):
    s = '\n'.join(v + "=" + str(contents[v]) for v in contents)
    with open("Parameter.txt","w") as wfile:
        wfile.write(s)

def WriteData(l):
    with codecs.open("B.txt","a","utf8") as f:
        f.writelines(l)

def UpdateCrawlerMain(PageNum):
    Continue = True
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
        for t in title:
            if str(t).find("<a href") >= 0:
                tObj = t.find_all("a")[0]
                subUrl.append(UHeader+tObj.get("href"))
                # print(tObj.text)
        # endregion

        # region UpdatePic
        for su in subUrl:
            l = SearchPicUrl(su)
            AddPicNum = AddPicNum + len(l)
            WriteData(l)
        # endregion
    # endregion

    # region Log
    d = Parameter()
    NewD = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")
    # Send Message
    if list(d.keys()).count('Update') is 0:
        d['Update'] = "None"
    msg = "Update Date : " + d['Update'] + "->" + NewD
    msg = msg + "\n" + "Add " + str(AddPicNum) + " Picture"

    d['Update'] = NewD
    WriteParameter(d)
    # endregion
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
def AddJpg():
    # 目前B.txt累積兩次Update(手動更新)，尋找.png的檔案為第二次的開始
    with codecs.open("B.txt","r","utf8") as r:
        l = list(row.replace("\n", "") + ".jpg\n" for row in r.readlines())
    with codecs.open("B.txt","w","utf8") as f:
        f.writelines(l)
# endregion

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])
    # UpdateCrawlerMain(10)
    # AddJpg()
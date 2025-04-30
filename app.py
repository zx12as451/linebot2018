# encoding: utf-8
import os
import random
from bs4 import BeautifulSoup
import requests
import time
import datetime
import codecs
import json
import logging

logging.basicConfig(level=logging.INFO)

from flask import Flask, request, abort, send_from_directory, jsonify, render_template

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

from yt_downloader_utils import download_youtube_video

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

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
    # print(event)
    # print(MessageEvent)
    # print("UserID", event.source.user_id)
    # print("GroupID", event.source.group_id)
    print("Handle: reply_token: " + event.reply_token + ", message: " + event.message.text)
    # content = "{}: {}".format(event.source.user_id, event.message.text)
    if event.message.text.find("更新") == 0:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="需要一段時間，請稍後......更新完成另發通知!!"))

        # UpdMsg = UpdatePTTBeauty(0)
        FlowerMain(event.message.text)
        
        if event.source.type == 'group':
            TargetID = event.source.group_id
        elif event.source.type == 'user':
            TargetID = event.source.user_id
        elif event.source.type == 'room':
            TargetID = event.source.room_id
        else:
            TargetID = None
            
        print("TargetID = " + TargetID)
        line_bot_api.push_message(
            TargetID,
            TextSendMessage(text='更新完成OK')
        )
    elif event.message.text == "檢查":
        contents = Parameter()
        s = '\n'.join(v + "=" + str(contents[v]) for v in contents)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=s))

    elif str(event.message.text).find("特抽") != -1:  # 是否含有"特抽"
        if str(event.message.text).find("特抽") != -1: # 是否含有"特抽"
            FilterMsg = str(event.message.text).replace("特抽","")  # 取代後的訊息
            Num = intTry(FilterMsg) # 取代後訊息是否能轉換成數值
            print(Num, "次")
            line_bot_api.reply_message(
                event.reply_token,
                returnContent(event.message.text,Num,"特"))

    elif event.message.text == "重複":
        Message = []
        Message.append(TextSendMessage(text=DelRepeat("Flower", "Flower.txt")))
        Message.append(TextSendMessage(text=DelRepeat("PTTBeauty", "B.txt")))
        line_bot_api.reply_message(
            event.reply_token,
            Message)
    else:
        if str(event.message.text).find("抽") != -1: # 是否含有"抽"
            FilterMsg = str(event.message.text).replace("抽","")  # 取代後的訊息
            Num = intTry(FilterMsg) # 取代後訊息是否能轉換成數值
            print(Num, "次")
            line_bot_api.reply_message(
                event.reply_token,
                returnContent(event.message.text,Num))
        else:
            # /mp3 https://...
            msg = event.message.text.strip()
            if msg.startswith("/mp3 ") or msg.startswith("/mp4 "):
                fmt = "mp3" if msg.startswith("/mp3") else "mp4"
                url = msg.split(" ", 1)[1]
                print("get mp3 or mp4.  url = ", url)

                try:
                    file_path = download_youtube_video(url, output_dir="/tmp", format=fmt)

                    if fmt == "mp4":
                        line_bot_api.reply_message(event.reply_token, VideoSendMessage(
                            original_content_url=f"https://yourdomain.com/downloads/{os.path.basename(file_path)}",
                            preview_image_url="https://yourdomain.com/static/preview.jpg"  # 可用預覽圖
                        ))
                    else:
                        line_bot_api.reply_message(event.reply_token, AudioSendMessage(
                            original_content_url=f"https://yourdomain.com/downloads/{os.path.basename(file_path)}",
                            duration=240000  # 以毫秒計算，可自行偵測音訊長度
                        ))
                except Exception as e:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"❌ 下載失敗: {str(e)}"))


@app.route("/")
def index():
    print("✅ 測試 log 是否出現", flush=True)
    logging.info("home page")
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    data = request.json
    url = data.get("url")
    fmt = data.get("format", "mp4")

    if not url:
        return jsonify({"error": "缺少 URL"}), 400

    try:
        file_path = download_youtube_video(url, output_dir=DOWNLOAD_FOLDER, format=fmt)
        filename = os.path.basename(file_path)
        download_url = request.url_root + "downloads/" + filename
        return jsonify({"success": True, "url": download_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/downloads/<filename>")
def serve_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)


def returnContent(U_Receive,Times,type="普通"):
    # C = TextSendMessage(text=U_Receive)
    if str(U_Receive).find("抽") != -1:
        if Times <= 5:
            lst = []
            for i in range(Times):
                img = RandomPic(type)
                C = ImageSendMessage(
                    # type='image',
                    original_content_url=img,  # Pic Url
                    preview_image_url=img  # Preview Pic
                )
                lst.append(C)
                print(img, i,"/",Times, "次")
            return lst
def RandomPic(type):
    img = "https://m1.ablwang.com/uploadfile/2017/0901/20170901042508280.jpg"
    filePath = "Flower.txt" if type == "特" else "B.txt"
    with open(filePath,"r") as file:
        d = file.read()
        l = d.split("\n")
        img = random.choice(l)
    return img

# region Update Pic DataBase

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
def Parameter():
    with open("Parameter.txt", "r") as file:
        s = file.read().replace("\n", "=")
        return Str2Dict(s, "=")
def WriteParameter(contents):
    s = '\n'.join(v + "=" + str(contents[v]) for v in contents)
    with codecs.open("Parameter.txt", "a","utf8") as wfile:
        wfile.write(s + "\n")
def Log(Type, AddPicNum):
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
    print("[" + Type + "]_" + NewD + " Total " + str(TotalPic) + " Insert " + str(AddPicNum))
    d['Update'] = "[" + Type + "]_" + NewD + " Total " + str(TotalPic) + " Insert " + str(AddPicNum)

    WriteParameter(d)
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
    # event.message.text = "更新-19403052-3"
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

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'], debug=True)
    # UpdateCrawlerMain(10)
    # AddJpg()
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
    line_bot_api.reply_message(
        event.reply_token,
        returnContent(event.message.text))


import os
def returnContent(U_Receive,Mode=""):
    C = TextSendMessage(text=U_Receive)
    if Mode is "img" or U_Receive == "抽":
        img = RandomPic()
        C = ImageSendMessage(
            type='image',
            original_content_url=img,  # Pic Url
            preview_image_url=img  # Preview Pic
        )
    return C

def RandomPic():
    img = "https://m1.ablwang.com/uploadfile/2017/0901/20170901042508280.jpg"
    return img

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])
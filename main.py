import os
import sys
import logging
from linebot import (
    LineBotApi, WebhookParser
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
from linebot.exceptions import (
    InvalidSignatureError
)

channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)

def callback(request):
    try:
        # 取得事件JSON
        signature = request.headers['X-Line-Signature']
        body = request.get_data(as_text=True)
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return 'ERROR'
        
        for event in events:
            handleEvent(event)

    # 在主控台Debug
    except:
        logging.error(sys.exc_info())
        return 'ERROR'
    return 'OK'

def handleEvent(event):
    if not isinstance(event, MessageEvent):
        return
    if not isinstance(event.message, TextMessage):
        return

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )
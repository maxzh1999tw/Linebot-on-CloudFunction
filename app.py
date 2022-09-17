from linebot import (LineBotApi, WebhookParser)
from google.cloud import firestore
from controllers import *


class LineBotApp:
    def __init__(self, channel_secret: str, channel_access_token: str):
        self.lineBotApi = LineBotApi(channel_access_token)
        self.parser = WebhookParser(channel_secret)

    def getEvents(self, request):
        signature = request.headers['X-Line-Signature']
        body = request.get_data(as_text=True)
        return self.parser.parse(body, signature)

    def serve(self, request):
        events = self.getEvents(request)
        try:
            # 一個 Request 啟用一條 DB 連線
            db = firestore.Client()
            self.db = db
            for event in events:
                self.Route(event)
        finally:
            db.close()

    def Route(self, event):
        # 一個事件使用一個 Controller
        if isinstance(event, FollowEvent) or isinstance(event, UnfollowEvent):
            FollowController(self.lineBotApi, self.db).handleEvent(event)
            return

        DefaultController(self.lineBotApi, self.db).handleEvent(event)

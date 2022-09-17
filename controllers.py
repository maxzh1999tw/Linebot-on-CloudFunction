from linebot import LineBotApi
from linebot.models import *
from google.cloud.firestore import Client
from models import *

from services import UserService
from views import View, ViewFactory


class BaseController:
    def __init__(self, lineBotApi: LineBotApi, db: Client, userService=None):
        self._db = db
        self.lineBotApi = lineBotApi
        self.userService = UserService(db) if userService == None else userService

    def recordAndReply(self, view: View):
        self.lineBotApi.reply_message(self.event.reply_token, view.message)
        self.userService.setLastMessageId(self.userId, view.messageId)

    def handleEvent(self, event):
        self.event = event
        self.userId = event.source.user_id

    def removeUserData(self):
        self.userService.removeUserData(self.userId)

    def getUserName(self, userId):
        return self.lineBotApi.get_profile(userId).display_name

class FollowController(BaseController):
    def __init__(self, lineBotApi: LineBotApi, db: Client, userService=None):
        super().__init__(lineBotApi, db, userService)

    def handleEvent(self, event):
        super().handleEvent(event)
        if isinstance(event, FollowEvent):
            self.recordAndReply(ViewFactory.greeting())
        elif isinstance(event, UnfollowEvent):
            self.removeUserData()

class DefaultController(BaseController):
    def __init__(self, lineBotApi: LineBotApi, db: Client, userService=None):
        super().__init__(lineBotApi, db, userService)

    def handleEvent(self, event):
        super().handleEvent(event)

        if isinstance(event, PostbackEvent):
            data = PostbackData.parse(event.postback.data)
            if not self.userService.isLastMessage(self.userId ,data.messageId): return

            elif data.id == PostbackDataId.Hello:
                self.recordAndReply(ViewFactory.askName())
                self.userService.setContext(self.userId, UserContext(UserContextId.AskName))
                return

        elif isinstance(event, MessageEvent):
            userContext = self.userService.getContext(self.userId)
            if userContext != None:
                if userContext.id == UserContextId.AskName:
                    if isinstance(event.message, TextMessage):
                        self.recordAndReply(ViewFactory.askNameReply(event.message.text, self.getUserName(self.userId)))
                        self.userService.setContext(self.userId, None)
                    else:
                        self.recordAndReply(ViewFactory.askName())
                    return

        self.recordAndReply(ViewFactory.greeting())
from linebot import LineBotApi
from linebot.models import *
from google.cloud.firestore import Client
from models import *

from services import UserService
from views import View, ViewFactory


class BaseController:
    def __init__(self, lineBotApi: LineBotApi, db: Client):
        self._db = db
        self._lineBotApi = lineBotApi

    def _getUserName(self, userId):
        return self._lineBotApi.get_profile(userId).display_name

    def handleEvent(self, event):
        self._event = event
        self._userId = event.source.user_id
        self._userService = UserService(self._db, self._userId)

    def _recordAndReply(self, view: View):
        self._lineBotApi.reply_message(self._event.reply_token, view.message)
        self._userService.lastMessageId = view.messageId

    def _removeUserData(self):
        self._userService.removeUserData(self._userId)


class FollowController(BaseController):
    def __init__(self, lineBotApi: LineBotApi, db: Client):
        super().__init__(lineBotApi, db)

    def handleEvent(self, event):
        super().handleEvent(event)
        if isinstance(event, FollowEvent):
            self._recordAndReply(ViewFactory.greeting())
        elif isinstance(event, UnfollowEvent):
            self._removeUserData()

class DefaultController(BaseController):
    def __init__(self, lineBotApi: LineBotApi, db: Client):
        super().__init__(lineBotApi, db)

    def handleEvent(self, event):
        super().handleEvent(event)

        if isinstance(event, PostbackEvent):
            data = PostbackData.parse(event.postback.data)
            if self._userService.lastMessage != data.messageId: return

            elif data.id == PostbackDataId.Hello:
                self._recordAndReply(ViewFactory.askName())
                self._userService.context = UserContext(UserContextId.AskName)
                return

        elif isinstance(event, MessageEvent):
            if self._userService.context != None:
                if self._userService.context.id == UserContextId.AskName:
                    if isinstance(event.message, TextMessage):
                        self._recordAndReply(ViewFactory.askNameReply(event.message.text, self._getUserName(self._userId)))
                        self._userService.context = None
                    else:
                        self._recordAndReply(ViewFactory.askName())
                    return

        self._recordAndReply(ViewFactory.greeting())
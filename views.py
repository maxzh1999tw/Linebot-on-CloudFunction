import uuid
from linebot.models import *

from models import PostbackData, PostbackDataId


class View:
    def __init__(self, messageId: str, message):
        self.messageId = messageId
        self.message = message

def newMessageId():
    return str(uuid.uuid4())

class ViewFactory:

    def greeting():
        messageId = newMessageId()
        postbackDataJson = PostbackData(PostbackDataId.Hello, messageId).toFormatedJSON()

        message = BubbleContainer(
            body=BoxComponent(
                layout="vertical",
                contents=[
                    TextComponent(text="Hay Man!")
                ]
            ),
            footer=BoxComponent(
                layout="vertical",
                contents=[
                    ButtonComponent(
                        action=PostbackAction(
                            label="Hello!",
                            data=postbackDataJson
                        )
                    )
                ]
            )
        )
        return View(messageId, FlexSendMessage(alt_text="Hay Man!", contents=message))

    def askName():
        messageId = newMessageId()
        return View(messageId, TextSendMessage(text="What's your name?"))

    def askNameReply(inputName: str, lineDisplayName: str):
        messageId = newMessageId()
        text = f"oh~ {inputName}~ what a good name!" if inputName == lineDisplayName else f"{inputName}? But your display name in LINE is {lineDisplayName}"
        return View(messageId, TextSendMessage(text=text))
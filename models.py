import json

class PostbackData:
    def __init__(self, id:str, messageId="", params=None):
        self.id = id
        self.messageId = messageId
        self.params = params

    def toFormatedJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4, separators=(',', ':')).replace("\"", "\\\"").replace("\n","")

    def parse(value: str):
        return json.loads(value.replace("\\\"", "\""), object_hook=lambda d: PostbackData(**d))

class PostbackDataId:
    Hello = "Hello"

class UserContext:
    def __init__(self, id: str, params=None):
        self.id = id
        self.params = params

    def __iter__(self):
        for key in self.__dict__:
            yield key, getattr(self, key)
    
    def parse(obj: dict):
        return UserContext(**obj) if obj != None else None

class UserContextId:
    AskName = "AskName"
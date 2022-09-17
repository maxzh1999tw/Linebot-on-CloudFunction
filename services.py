from google.cloud.firestore import Client

from models import UserContext

class UserService:

    def __init__(self, db: Client):
        self._db = db
        self._collection = self._db.collection("User")

    def setLastMessageId(self, userId: str, messageId: str):
        self._collection.document(userId).set({
            "LastMessageId": messageId
        }, merge=True)

    def isLastMessage(self, userId: str, messageId: str) -> bool:
        doc = self._collection.document(userId).get()
        if not doc.exists:
            return False
        return messageId == doc.get("LastMessageId")

    def removeUserData(self, userId):
        doc = self._collection.document(userId)
        if doc.get().exists:
            doc.delete()

    def getContext(self, userId: str):
        doc = self._collection.document(userId).get()
        if not doc.exists:
            return None
        dict = doc.to_dict()
        return UserContext.parse(dict["Context"]) if "Context" in dict else None

    def setContext(self, userId: str, context: UserContext):
        self._collection.document(userId).set({
            "Context": dict(context) if context != None else None
        }, merge = True)
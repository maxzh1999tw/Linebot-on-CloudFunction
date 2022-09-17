from google.cloud.firestore import Client, DocumentReference

from models import UserContext

def tryGetDocField(docRef: DocumentReference, field: str, default = None):
        doc = docRef.get()
        if doc.exists:
            docDict = doc.to_dict()
            return docDict[field] if field in docDict else default
        return default

class UserService:
    def __init__(self, db: Client, userId):
        self._db = db
        self._userId = userId
        self._document = self._db.collection("User").document(userId)
        self._lastMessageId = None
        self._context = None

    def removeUserData(self):
        self._document.delete()

    @property
    def lastMessage(self):
        if self._lastMessageId != None:
            return self._lastMessageId
        else:
            return tryGetDocField(self._document, "LastMessageId")

    @lastMessage.setter
    def lastMessageId(self, messageId: str):
        self._lastMessageId = messageId
        self._document.set({
            "LastMessageId": messageId
        }, merge=True)
    
    @property
    def context(self):
        if self._context != None:
            return self._context
        else:
            contextField = tryGetDocField(self._document, "Context")
            return UserContext.parse(contextField) if contextField != None else None

    @context.setter
    def context(self, context: UserContext):
        self._context = context
        self._document.set({
            "Context": dict(context) if context != None else None
        }, merge = True)
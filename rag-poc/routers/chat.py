from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from dbs.database import get_db, ChatModel, MessageModel, ChunkModel
from routers.user import getCurrentUser, User
from core import rag
from fastapi import status

router = APIRouter()

class AddMessage(BaseModel):
    message: str
    chatID: int
    userID: int

class RenameChat(BaseModel):
    chatName: str
    chatID: int

@router.post("/chat")
async def chat(chat: AddMessage, db: Session = Depends(get_db), user: User = Depends(getCurrentUser)):
    activeChat = None
    if chat.chatID == 0:
        activeChat = ChatModel(userID=chat.userID, name="neuer Chat")
        db.add(activeChat)
        db.commit()
        db.refresh(activeChat)
    else:
        activeChat = db.query(ChatModel).filter(ChatModel.id == chat.chatID).first()
    if activeChat:
        newUserMessage = MessageModel(message=chat.message, sources='', chatID=activeChat.id, author="user")
        db.add(newUserMessage)
        db.commit()
        msg = await queryEndpoint(chat.message)
        message = msg['response']
        sources = str(msg['sources'])
        newMessage = MessageModel(message=message, sources=sources, chatID=activeChat.id, author="system")
        db.add(newMessage)
        db.commit()
        db.refresh(newUserMessage)
        db.refresh(newMessage)
        return {"chatID": activeChat.id, "name": activeChat.name, "chat": activeChat.messages}
    else:
        raise HTTPException(status_code=404, detail=f"Fehler, kein Chat mit dieser ID gefunden: {str(e)}")
    
    return newMessage

@router.post("/rename_chat")
async def renameChat(data: RenameChat, db: Session = Depends(get_db), user: User = Depends(getCurrentUser)):
    activeChat = db.query(ChatModel).filter(ChatModel.id == data.chatID).first()
    if activeChat:
        activeChat.name = data.chatName
        db.commit()
        db.refresh(activeChat)
        return activeChat
    else:
        raise HTTPException(status_code=404, detail=f"Fehler, kein Chat gefunden: {str(e)}")

@router.get("/chat")
async def getMSGsByChat(chatID: int, db: Session = Depends(get_db), user: User = Depends(getCurrentUser)):
    chat = db.query(MessageModel).filter(MessageModel.chatID == chatID).all()
    if not chat:
        return []
    return chat

@router.get("/user_chats")
async def getChatsByUser(userID: int, db: Session = Depends(get_db), user: User = Depends(getCurrentUser)):
    chats = db.query(ChatModel).filter(ChatModel.userID == userID).all()
    return chats

@router.post("/delete_chat")
async def deleteChat(chatID: int, db: Session = Depends(get_db), user: User = Depends(getCurrentUser)):
    chat = db.query(ChatModel).filter(ChatModel.id == chatID).first()
    if not chat:
        raise HTTPException(status_code=404, detail=f"Fehler, kein Chat gefunden: {str(e)}")

    msgs = db.query(MessageModel).filter(MessageModel.chatID == chatID).all()
    for msg in msgs:
        db.delete(msg)

    db.delete(chat)
    db.commit()
    return {"message": "Chat erfolgreich entfernt"}

@router.post("/query")
async def queryEndpoint(msg: str, user: User = Depends(getCurrentUser)):
    response = rag.queryMulti(msg)
    return response

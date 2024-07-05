from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, ChatModel, MessageModel, ChunkModel
import rag 

router = APIRouter()

class AddMessage(BaseModel):
    message: str
    chatID: int
    userID: int

class RenameChat(BaseModel):
    chatName: str
    chatID: int

@router.post("/chat")
async def chat(chat: AddMessage):
    try:
        session = SessionLocal()
        if chat.chatID == 0:
            activeChat = ChatModel(userID=chat.userID, name="new Chat")
            session.add(activeChat)
            session.commit()
        else:
            activeChat = session.query(ChatModel).filter(ChatModel.id == chat.chatID).first()

        if activeChat:
            newUserMessage = MessageModel(message=chat.message, sources='', chatID=activeChat.id, author="user")
            msg = await query_endpoint(chat.message)
            message = msg['response']
            sources = str(msg['sources'])
            newMessage = MessageModel(message=message, sources=sources, chatID=activeChat.id, author="system")
            session.add(newUserMessage)
            session.add(newMessage)
            session.flush()
            session.commit()
            if chat.chatID != 0:
                session.refresh(newUserMessage)
                session.refresh(newMessage)
                return newMessage
        else:
            print("no chat with this id")
        return {"chatID": activeChat.id, "name": activeChat.name, "chat": activeChat.messages}
    finally:
        session.close()

@router.post("/rename_chat")
async def rename_chat(data: RenameChat):
    try:
        session = SessionLocal()
        activeChat = session.query(ChatModel).filter(ChatModel.id == data.chatID).first()
        if activeChat:
            activeChat.name = data.chatName
            session.commit()
            session.refresh(activeChat)
            return activeChat
    finally:
        session.close()

@router.get("/chat")
async def get_msgs_by_chat(chatID: int):
    try:
        session = SessionLocal()
        chat = session.query(MessageModel).filter(MessageModel.chatID == chatID).all()
        if not chat:
            return []
        return chat
    finally:
        session.close()

@router.get("/user_chats")
async def get_chats_by_user(userID: int):
    try:
        session = SessionLocal()
        chats = session.query(ChatModel).filter(ChatModel.userID == userID).all()
        return chats
    finally:
        session.close()

@router.post("/delete_chat")
async def delete_chat(chatID: int):
    try:
        session = SessionLocal()
        chat = session.query(ChatModel).filter(ChatModel.id == chatID).first()
        if not chat:
            raise HTTPException(status_code=404, detail="Chat not found")

        msgs = session.query(MessageModel).filter(MessageModel.chatID == chatID).all()
        for msg in msgs:
            session.delete(msg)

        session.delete(chat)
        session.commit()
        return {"message": "Chat deleted successfully"}
    finally:
        session.close()

@router.post("/query")
async def query_endpoint(msg: str):
    response = rag.query(msg)
    # try:
    #     session = SessionLocal()
    #     sources = []
    #     for source in response['sources']: 
    #       chunk = session.query(ChunkModel).filter(ChunkModel.chunkID == source).first()
    #       print(chunk.content)
    #       sources.append({'chunkID': chunk.chunkID, 'content': chunk.content})

    #     return {"response": response['response'], "sources": sources}
    # finally:
    #     session.close()

    return response

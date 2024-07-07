from sqlalchemy import create_engine, Column, Integer, String, Boolean, LargeBinary, MetaData, ForeignKey
from sqlalchemy.dialects.mysql import LONGBLOB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import config

DATABASE_URL = config.dburl
Base = declarative_base()
engine = create_engine(DATABASE_URL, pool_recycle=3600)
connection = engine.connect()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(32), unique=True, nullable=False)
    pw = Column(String(128), nullable=False)
    chats = relationship("ChatModel", back_populates="user", cascade="all, delete-orphan")

class MessageModel(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    message = Column(String(4096), nullable=False)
    sources = Column(String(512), nullable=True)
    author = Column(String(16), nullable=False)
    chatID = Column(Integer, ForeignKey('chats.id', ondelete='CASCADE'), nullable=False)
    chat = relationship("ChatModel", back_populates="messages")

class ChatModel(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(64), index=True)
    userID = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = relationship("UserModel", back_populates="chats")
    messages = relationship("MessageModel", back_populates="chat", cascade="all, delete-orphan")

class DocumentModel(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(64), index=True)
    content = Column(LONGBLOB)
    chunks = relationship("ChunkModel", back_populates="document", cascade="all, delete-orphan")
    
class ChunkModel(Base):
    __tablename__ = "chunks"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    chunkID = Column(String(128), index=True)
    content = Column(LargeBinary)
    documentID = Column(Integer, ForeignKey('documents.id', ondelete='CASCADE'))
    document = relationship("DocumentModel", back_populates="chunks")

Base.metadata.create_all(bind=engine)

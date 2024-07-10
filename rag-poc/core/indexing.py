import config
from sqlalchemy.orm import Session
from dbs.database import SessionLocal, DocumentModel, ChunkModel, UserModel, ChatModel, MessageModel
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader

def loadData():
    documents = getDocumentsFromSQL()
    for doc in documents:
        persist(documents)

def getDocumentsFromSQL():
    session = SessionLocal()
    try:
        documents = session.query(DocumentModel).all()
        return [Document(page_content=doc.content.decode('utf-8'), metadata={"name": doc.name}) for doc in documents]
    finally:
        session.close()

def persist(document: Document, documentID):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.splitter['chunk_size'],
        chunk_overlap=config.splitter['chunk_overlap'],
        length_function=config.splitter['length_function'],
        is_separator_regex=config.splitter['is_separator_regex'],
    )
    chunks = splitter.split_documents(document)
    db = config.getDB()
    chunkIDs = getChunkIDs(chunks)
    items = db.get(include=[])
    ids = set(items["ids"])
    newChunks = []

    try:
        session = SessionLocal()
        for chunk in chunkIDs:
            if chunk.metadata["id"] not in ids:
                newChunks.append(chunk)
                chunkModelObject = ChunkModel(documentID=documentID, chunkID=chunk.metadata["id"], content=chunk.page_content.encode('utf-8'))
                session.add(chunkModelObject)
        session.commit()
        session.refresh(chunkModelObject)
    except Exception as e:
        return {"error": str(e)}
    finally:
        session.close()

        if len(newChunks):
            chunkIDs = [chunk.metadata["id"] for chunk in newChunks]
            db.add_documents(newChunks, ids=chunkIDs)
        else:
            print("No new documents to upload")
        
def getChunkIDs(chunks):
    lastPageID = None
    index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        pageID = f"{source}:{page}"

        if pageID == lastPageID:
            index += 1
        else:
            index = 0

        chunkID = f"{pageID}:{index}"
        lastPageID = pageID
        chunk.metadata["id"] = chunkID

    return chunks

def loadDocument(file_path: str):
    ext = os.path.splitext(file_path)[-1].lower()
    dID = None
    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
    elif ext == ".txt":
        loader = TextLoader(file_path)
    elif ext == ".html":
        loader = HTMLLoader(file_path)
    else:
        raise ValueError("Unsupported file type")

    try:
        session = SessionLocal()
        with open(file_path, "rb") as f:
            content = f.read()
            document = DocumentModel(name=os.path.basename(file_path), content=content)
            session.add(document)
            session.commit()
            dID=document.id
            session.refresh(document)
    except Exception as e:
        return {"error": str(e)}
    finally:
        session.close()
        
    document = loader.load()
    persist(document, dID)
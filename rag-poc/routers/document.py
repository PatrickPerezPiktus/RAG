from fastapi import APIRouter, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, DocumentModel, ChunkModel
import indexing
import os
import shutil
from typing import List

router = APIRouter()

@router.get("/load_data")
async def load_data_endpoint():
    indexing.loadData()
    return {"message": "Indexing der lokalen Daten"}

@router.post("/add")
async def add_document(file: UploadFile = File(...)):
    file_path = f"temp/{file.filename}"
    os.makedirs("temp", exist_ok=True)
    try:
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        indexing.loadDocument(file_path)
        os.remove(file_path)
        return {"message": f"Document {file.filename} added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/documents")
async def get_documents():
    try:
        session = SessionLocal()
        documents = session.query(DocumentModel).all()
        return {"documents": [{"id": doc.id, "name": doc.name} for doc in documents]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

@router.get("/documents_with_chunks")
async def get_documents_with_chunks():
    try:
        session = SessionLocal()
        documents = session.query(DocumentModel).all()
        response = []
        for doc in documents:
            chunks = session.query(ChunkModel).filter(ChunkModel.documentID == doc.id).all()
            response.append({
                "id": doc.id,
                "name": doc.name,
                "chunks": [{"id": chunk.id, "chunkID": chunk.chunkID, "content": chunk.content.decode('utf-8')} for chunk in chunks]
            })
        return {"documents": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

class ChunkIDList(BaseModel):
    chunkIDs: List[str]

@router.post("/load_chunks")
async def load_chunks(chunk_id_list: ChunkIDList):
    try:
        session = SessionLocal()
        chunks = session.query(ChunkModel).filter(ChunkModel.chunkID.in_(chunk_id_list.chunkIDs)).all()
        if not chunks:
            raise HTTPException(status_code=404, detail="Chunks not found")
        return {"chunks": [{"id": chunk.id, "chunkID": chunk.chunkID, "content": chunk.content.decode('utf-8')} for chunk in chunks]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

@router.get("/load_chunk_by_id")
async def load_chunks(chunkID: str):
    try:
        session = SessionLocal()
        chunk = session.query(ChunkModel).filter(ChunkModel.chunkID == chunkID).first()
        if not chunk:
            raise HTTPException(status_code=404, detail="Chunk not found")
        return {"chunkID": chunk.chunkID, "content": chunk.content.decode('utf-8')}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()
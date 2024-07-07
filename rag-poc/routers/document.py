from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from dbs.database import get_db, DocumentModel, ChunkModel
from routers.user import get_current_user, User
from core import indexing
import os
import shutil
from typing import List

router = APIRouter()

@router.get("/load_data")
async def load_data_endpoint(user: User = Depends(get_current_user)):
    try:
        indexing.loadData()
        return {"message": "Indexing der lokalen Daten"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fehler beim Laden der Daten: {str(e)}")

@router.post("/add")
async def add_document(file: UploadFile = File(...), user: User = Depends(get_current_user)):
    file_path = f"temp/{file.filename}"
    os.makedirs("temp", exist_ok=True)
    try:
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        indexing.loadDocument(file_path)
        os.remove(file_path)
        return {"message": f"Document {file.filename} added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fehler beim Hinzufügen des Dokuments: {str(e)}")

@router.get("/documents")
async def get_documents(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        documents = db.query(DocumentModel).all()
        return {"documents": [{"id": doc.id, "name": doc.name} for doc in documents]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fehler beim Abrufen der Dokumente: {str(e)}")

@router.get("/documents_with_chunks")
async def get_documents_with_chunks(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        documents = db.query(DocumentModel).all()
        response = []
        for doc in documents:
            chunks = db.query(ChunkModel).filter(ChunkModel.documentID == doc.id).all()
            response.append({
                "id": doc.id,
                "name": doc.name,
                "chunks": [{"id": chunk.id, "chunkID": chunk.chunkID, "content": chunk.content.decode('utf-8')} for chunk in chunks]
            })
        return {"documents": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fehler beim Abrufen der Dokumente mit Chunks: {str(e)}")

class ChunkIDList(BaseModel):
    chunkIDs: List[str]

@router.post("/load_chunks")
async def load_chunks(chunk_id_list: ChunkIDList, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        chunks = db.query(ChunkModel).filter(ChunkModel.chunkID.in_(chunk_id_list.chunkIDs)).all()
        if not chunks:
            raise HTTPException(status_code=404, detail="Chunks not found")
        return {"chunks": [{"id": chunk.id, "chunkID": chunk.chunkID, "content": chunk.content.decode('utf-8')} for chunk in chunks]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fehler beim Laden der Chunks: {str(e)}")

@router.get("/load_chunk_by_id")
async def load_chunk_by_id(chunkID: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        chunk = db.query(ChunkModel).filter(ChunkModel.chunkID == chunkID).first()
        if not chunk:
            raise HTTPException(status_code=404, detail="Chunk not found")
        return {"chunkID": chunk.chunkID, "content": chunk.content.decode('utf-8')}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fehler beim Laden des Chunks: {str(e)}")

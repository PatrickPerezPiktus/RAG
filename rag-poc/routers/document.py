from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from dbs.database import get_db, DocumentModel, ChunkModel
from routers.user import getCurrentUser, User
from core import indexing
import config
import os
import shutil
from typing import List
import numpy as np
from sklearn.decomposition import PCA
from umap import UMAP

router = APIRouter()

@router.get("/load_data")
async def loadData(user: User = Depends(getCurrentUser)):
    try:
        indexing.loadData()
        return {"message": "Indexing der lokalen Daten"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fehler beim Laden der Daten: {str(e)}")

@router.post("/add")
async def addDocument(file: UploadFile = File(...), user: User = Depends(getCurrentUser)):
    file_path = f"{file.filename}"
    os.makedirs("temp", exist_ok=True)
    try:
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        indexing.loadDocument(file_path)
        os.remove(file_path)
        return {"message": f"Dokument {file.filename} erfolgreich hinzugefügt"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fehler beim Hinzufügen des Dokuments: {str(e)}")

@router.get("/load_confluence")
async def loadConfluence(): #user: User = Depends(getCurrentUser)
    try:
        indexing.laodConfluence()
        return {"message": "Indexing der Confluence Daten"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fehler beim Laden der Confluence-Daten: {str(e)}")

@router.get("/reset")
async def resetDBs(): #user: User = Depends(getCurrentUser)
    try:
        data = indexing.laodConfluence()
        return {"confluenceData": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fehler beim Laden der Confluence-Daten: {str(e)}")

@router.get("/documents")
async def getDocuments(db: Session = Depends(get_db), user: User = Depends(getCurrentUser)):
    try:
        documents = db.query(DocumentModel).all()
        return {"documents": [{"id": doc.id, "name": doc.name} for doc in documents]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fehler beim Abrufen der Dokumente: {str(e)}")

@router.get("/documents_with_chunks")
async def getDocumentsWithChunks(db: Session = Depends(get_db), user: User = Depends(getCurrentUser)):
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
async def loadChunks(chunk_id_list: ChunkIDList, db: Session = Depends(get_db), user: User = Depends(getCurrentUser)):
    try:
        chunks = db.query(ChunkModel).filter(ChunkModel.chunkID.in_(chunk_id_list.chunkIDs)).all()
        if not chunks:
            raise HTTPException(status_code=404, detail="Chunks not found")
        return {"chunks": [{"id": chunk.id, "chunkID": chunk.chunkID, "content": chunk.content.decode('utf-8')} for chunk in chunks]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fehler beim Laden der Chunks: {str(e)}")

@router.get("/load_chunk_by_id")
async def loadChunkByID(chunkID: str, db: Session = Depends(get_db), user: User = Depends(getCurrentUser)):
    try:
        chunk = db.query(ChunkModel).filter(ChunkModel.chunkID == chunkID).first()
        if not chunk:
            raise HTTPException(status_code=404, detail="Chunk not found")
        return {"chunkID": chunk.chunkID, "content": chunk.content.decode('utf-8')}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fehler beim Laden des Chunks: {str(e)}")

@router.get("/embedded_data")
async def getEmbeddedData(): #user: User = Depends(getCurrentUser) TODO 
    try:
        data = config.getDB().get(include=["embeddings"])
        embeddings = np.array(data['embeddings'])
        pca = PCA(n_components=3)
        reduced_embeddings = pca.fit_transform(embeddings)
        return {'ids': data['ids'], 'vectors': reduced_embeddings.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fehler beim Abrufen der Vektor-Daten: {str(e)}")

@router.get("/embedded_data_umap")
async def getEmbeddedDataUMAP():  # user: User = Depends(getCurrentUser) TODO
    try:
        data = config.getDB().get(include=["embeddings"])
        embeddings = np.array(data['embeddings'])

        umap = UMAP(n_components=3)
        reduced_embeddings = umap.fit_transform(embeddings)

        return {'ids': data['ids'], 'vectors': reduced_embeddings.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fehler beim Abrufen der Vektor-Daten: {str(e)}")

class EmbeddingMsg(BaseModel):
    test: str

@router.get("/embedded_data_umap_msg")
async def getEmbeddding(emb: EmbeddingMsg): #, user: User = Depends(getCurrentUser)#TODO
    embedding = indexing.getEmbedding(emb.text)
    try:
        data = config.getDB().get(include=["embeddings"])
        data['embeddings'].append(embedding)
        embeddings = np.array(data['embeddings'])

        umap = UMAP(n_components=3)
        reduced_embeddings = umap.fit_transform(embeddings)
        data['ids'].append(msg)
        return {'ids': data['ids'], 'vectors': reduced_embeddings.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fehler beim Abrufen der Vektor-Daten: {str(e)}")

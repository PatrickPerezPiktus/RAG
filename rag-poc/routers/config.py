from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from routers.user import get_current_user, User
import config

router = APIRouter()

class ConfigData(BaseModel):
    llm: str
    vectorDB: str
    embeddingModel: str
    dbPath: str
    dataDump: str
    k: int
    chunk_size: int
    chunk_overlap: int
    promptTemplate: str
    testPrompt: str

@router.post("/update_config")
async def update_config(config_data: ConfigData, user: User = Depends(get_current_user)):
    try:
        config.updateParameters(config_data)
        return {"message": "Konfiguration erfolgreich aktualisiert", "config": config.getParameters()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Die Konfiguration konnte nicht verändert werden: {str(e)}")

@router.get("/get_config")
async def get_config(user: User = Depends(get_current_user)):
    try:
        return {"config": config.getParameters()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Es ist ein Fehler beim laden der Konfiguration aufgetreten: {str(e)}")

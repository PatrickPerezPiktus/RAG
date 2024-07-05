from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
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
async def update_config(config_data: ConfigData):
    try:
        config.updateParameters(config_data)
        return {"message": "Konfiguration erfolgreich aktualisiert", "config": config.getParameters()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get_config")
async def get_config():
    try:
        return {"config": config.getParameters()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

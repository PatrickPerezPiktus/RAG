from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from routers.user import getCurrentUser, User
import config

router = APIRouter()

class ConfigData(BaseModel):
    llm: str
    vectorDB: str
    embeddingModel: str
    activeRAG: str
    
    k: int
    temperature: int
    chunk_size: int
    chunk_overlap: int

    promptTemplate: str
    multiQuery_template: str
    hyde_template: str

    llmOptions: list
    embeddingModelOptions: list
    vectorDBOptions: list
    RAGOptOptions: list


@router.post("/update_config")
async def updateConfig(config_data: ConfigData, user: User = Depends(getCurrentUser)):
    try:
        config.updateParameters(config_data)
        return {"message": "Konfiguration erfolgreich aktualisiert", "config": config.getParameters()}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Die Konfiguration konnte nicht verändert werden: {str(e)}")

@router.get("/get_config")
async def getConfig(user: User = Depends(getCurrentUser)):
    try:
        return {"config": config.getParameters()}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Es ist ein Fehler beim laden der Konfiguration aufgetreten: {str(e)}")

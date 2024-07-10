from fastapi.testclient import TestClient
from unittest.mock import patch
import config
from myapp import app  # Dein FastAPI-Anwendungsobjekt

client = TestClient(app)

def testUpdateConfig():
    new_config = {
        "llm": "new_llm",
        "vectorDB": "new_vectorDB",
        "embeddingModel": "new_embeddingModel",
        "dbPath": "new_dbPath",
        "dataDump": "new_dataDump",
        "k": 10,
        "chunk_size": 100,
        "chunk_overlap": 10,
        "promptTemplate": "new_promptTemplate",
        "testPrompt": "new_testPrompt"
    }

    with patch.object(config, 'updateParameters') as mock_update, patch.object(config, 'getParameters', return_value=new_config):
        response = client.post("/update_config", json=new_config)
        assert response.status_code == 200
        assert response.json() == {"message": "Konfiguration erfolgreich aktualisiert", "config": new_config}
        mock_update.assert_called_once_with(new_config)

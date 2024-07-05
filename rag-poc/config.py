from langchain_community.vectorstores import Chroma
from langchain_community.llms.ollama import Ollama
from langchain_openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from pydantic import BaseModel
import openai
import os
import json
import chromadb

load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']

dbPath = "database"
dburl = 'mysql+mysqlconnector://user:password@localhost:3306/ragdb'  
dataDump = "raw_data"
k = 3
activeDB = "chroma"
activeLLM = "openai"
activeEmbedding = "openai"

#from langchain_cohere import CohereEmbeddings

cohere_embeddings_model = "" #CohereEmbeddings(cohere_api_key=os.environ['COHERE_API_KEY'])

openai_embeddings_model = OpenAIEmbeddings()

embeddingModelList = dict(
    openai= openai_embeddings_model,
    cohere= cohere_embeddings_model
)

embeddingsmodel = embeddingModelList[activeEmbedding]

openaiLLM = OpenAI()
llamaLLM = ""# Ollama("llama3")
mistralLLM = "" #Ollama("mistral")
llmList = dict(
    openai= openaiLLM,
    mistral=mistralLLM
)
def getLLM():
    return llmList[activeLLM]

from langchain_pinecone import PineconeVectorStore

index_name = "langchain-test-index"
pinecone = ""#PineconeVectorStore.from_documents(docs, embeddings, index_name=index_name)

chroma_client = chromadb.HttpClient(host='localhost', port=8000)
collection = chroma_client.get_or_create_collection(name="games")
chroma = Chroma(persist_directory=dbPath, embedding_function=embeddingsmodel, client=chroma_client)
dbList = dict(
    chroma= chroma, 
    pinecone= pinecone 
)

db = dbList[activeDB]

splitter = dict(
    chunk_size=800,
    chunk_overlap=80,
    length_function=len,
    is_separator_regex=False,
)

promptTemplate = """
Beantworte die Frage nur auf der Grundlage des folgenden Kontextes:

{context}

---

Frage: {question}

---

Quellen: {sources}
"""



testPrompt = """
Expected Response: {expected}
Actual Response: {actual}
---
(Answer with 'true' or 'false') Does the actual response match the expected response? 
"""


def getParameters():
    params = {
        "llm": activeLLM,
        "vectorDB": activeDB,
        "embeddingModel": activeEmbedding,
        "dbPath": dbPath,
        "dataDump": dataDump,
        "k": k,
        "chunk_size":splitter["chunk_size"],
        "chunk_overlap":splitter["chunk_overlap"],
        "promptTemplate": promptTemplate.strip(),
        "testPrompt": testPrompt.strip(),
        "llmOptions": list(llmList.keys()),
        "embeddingModelOptions": list(embeddingModelList.keys()),
        "vectorDBOptions": list(dbList.keys()),
    }
    return params

class ConfigData(BaseModel):
    llm: int
    vectorDB: int
    embeddingModel: int
    dbPath: str
    dataDump: str
    k: int
    chunk_overlap: int
    chunk_overlap: int
    promptTemplate: str
    testPrompt: str

def updateParameters(params):
    global dbPath, dataDump, k, splitter, promptTemplate, testPrompt, activeDB, activeEmbedding, activeLLM
    
    activeDB = params.vectorDB
    activeLLM = params.llm
    activeEmbedding = params.embeddingModel
    dbPath = params.dbPath
    dataDump = params.dataDump
    k = params.k
    splitter["chunk_overlap"] = params.chunk_overlap
    splitter["chunk_size"] = params.chunk_size
    promptTemplate = params.promptTemplate
    testPrompt = params.testPrompt
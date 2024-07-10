from langchain_community.vectorstores import Chroma
from langchain_pinecone import PineconeVectorStore
from langchain_community.llms.ollama import Ollama
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from pydantic import BaseModel
import openai
import os
import json
import chromadb

# local Data
dataDump = "_raw_data"

# SQL-DB PATH 
sqldburl = 'mysql+mysqlconnector://user:password@localhost:3306/ragdb'

# ANN-Search-Val (Anzahl der Elemente)
k = 3

# .env vars 
load_dotenv()

# JSON Web Token Key 
jwt_secret_key = os.environ['JWT_SECRET_KEY']
hash_algo = "HS256"
token_expire_minutes = 90

# LANGSMITH API
langchain_tracing = os.environ['LANGCHAIN_TRACING_V2']
langchain_api_key = os.environ['LANGCHAIN_API_KEY']

# Confluence API
confluence_secret_key = os.environ['CONFLUENCE_SECRET_KEY']
confluence_user='tim.hardick@itc-studenten.de'
confluence_url='https://ragtest.atlassian.net/wiki/'
confluence_space='Spiele1'

### SPLITTER

# MarkDown-Splitter
headers_to_split_on = [
        ("#", ""),
        ("##", ""),
        ("###", ""),
    ]

# Text-Splitter
splitter = dict(
    chunk_size=800,
    chunk_overlap=80,
    length_function=len,
    is_separator_regex=False,
)

### EMBEDDING-MODELS
activeEmbedding = "openai"

# Cohere
cohere_embeddings_model = "" #CohereEmbeddings(cohere_api_key=os.environ['COHERE_API_KEY'])
# OpenAI
openai_embeddings_model = OpenAIEmbeddings()
# Local
local_embeddings_model = OllamaEmbeddings(model="mxbai-embed-large") 

embeddingModelList = dict(
    openai= openai_embeddings_model,
    cohere= cohere_embeddings_model,
    local= local_embeddings_model
)
embeddingsmodel = embeddingModelList[activeEmbedding]


## LLM 
activeLLM = "openai"

# OPENAI
openai.api_key = os.environ['OPENAI_API_KEY']
openaiLLM = ChatOpenAI(model="gpt-3.5-turbo-16k")
# Local Llama 
llamaLLM = Ollama(model="llama3")
# Local Mistral
mistralLLM = "" #Ollama("mistral")

llmList = dict(
    openai= openaiLLM,
    mistral=mistralLLM,
    llama=llamaLLM
)
def getLLM():
    return llmList[activeLLM]


# VEKTOR-DATENBANK
activeDB = "chroma"

#Pinecone
pinecone = ""#PineconeVectorStore.from_documents(docs, embeddings, index_name=index_name)
# Chroma
dbDirectory = "database"
chroma_client = chromadb.HttpClient(host='localhost', port=8000)
collection = chroma_client.get_or_create_collection(name="games")
chroma = Chroma(persist_directory=dbDirectory, embedding_function=embeddingsmodel, client=chroma_client)

dbList = dict(
    chroma= chroma, 
    pinecone= pinecone 
)
def getDB():
    return dbList[activeDB]


### PROMPTS 

# multiQuery-Prompt
multiQuery_template = """Du bist ein KI-Sprachmodell-Assistent. Deine Aufgabe ist es, fünf 
verschiedene Versionen der gegebenen Benutzerfrage zu generieren, um relevante Dokumente aus einer Vektordatenbank 
Datenbank zu finden. Ziel ist es einige der Einschränkungen der entfernungsbasierten Ähnlichkeitssuche zu überwinden,
indem du mehrere Perspektiven auf die Frage des Benutzers erzeugst.     
Gib diese alternativen Fragen durch Zeilenumbrüche getrennt aus.
Ursprüngliche Benutzerfrage: {question}"""

# RAG-Prompt 
promptTemplate = """
Du bist ein Assistent zur Beantwortung von Fragen im Bezug auf Versicherungsbedingungen. 
Damit du genaue Informationen geben kannst wird dir ein Kontext zur verfügung gestellt. 
Dieser Kontext wird aus Teilstücken von Dokumenten zusammengesetzt.
Beantworte die Frage auf der Grundlage des folgenden Kontextes:

{context}

---

Frage: {question}
"""

# Test-Prompt 
testPrompt = """
Expected Response: {expected}
Actual Response: {actual}
---
(Answer with 'true' or 'false') Does the actual response match the expected response? 
"""

### Konfuguration bereitstellen: 

def getParameters():
    params = {
        "llm": activeLLM,
        "vectorDB": activeDB,
        "embeddingModel": activeEmbedding,
        "sqldburl": sqldburl,
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
    sqldburl: str
    dataDump: str
    k: int
    chunk_overlap: int
    chunk_size: int
    promptTemplate: str
    testPrompt: str

def updateParameters(params):
    global sqldburl, dataDump, k, splitter, promptTemplate, testPrompt, activeDB, activeEmbedding, activeLLM
    
    activeDB = params.vectorDB
    activeLLM = params.llm
    activeEmbedding = params.embeddingModel
    sqldburl = params.sqldburl
    dataDump = params.dataDump
    k = params.k
    splitter["chunk_overlap"] = params.chunk_overlap
    splitter["chunk_size"] = params.chunk_size
    promptTemplate = params.promptTemplate
    testPrompt = params.testPrompt
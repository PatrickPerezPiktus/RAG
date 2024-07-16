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

### .env vars 
load_dotenv()

# SQL-DB PATH 
sqlUser = os.environ['SQL_USER']
sqlPW = os.environ['SQL_PW']
sqlServer = os.environ['SQL_SERVER']
sqldburl = 'mysql+mysqlconnector://'+sqlUser+':'+sqlPW+'@'+sqlServer+':3306/ragdb' 

# ANN-Search-Val (Anzahl der Elemente)
k = 3

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
cohere_api_key=os.environ['COHERE_API_KEY']
cohere_embeddings_model = '' #CohereEmbeddings(cohere_api_key)
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


### LLM 
activeLLM = "openai"

# OPENAI
temperature=0
openai.api_key = os.environ['OPENAI_API_KEY']
openaiLLM = ChatOpenAI(model="gpt-3.5-turbo-16k", temperature=temperature)
# Local Llama 
llamaLLM = Ollama(model="llama3")
# Local Mistral
mistralLLM = Ollama(model="mistral")

llmList = dict(
    openai=openaiLLM,
    mistral=mistralLLM,
    llama=llamaLLM
)
def getLLM():
    return llmList[activeLLM]


### VEKTOR-DATENBANK
activeDB = "chroma"

#Pinecone
pinecone = ""#PineconeVectorStore.from_documents(docs, embeddings, index_name=index_name)
# Chroma
dbDirectory = "database"
chromaServer = os.environ['CHROMA_SERVER']
chroma_client = chromadb.HttpClient(host=chromaServer, port=8000) 
chroma = Chroma(persist_directory=dbDirectory, embedding_function=embeddingsmodel, client=chroma_client)

dbList = dict(
    chroma=chroma, 
    #pinecone=pinecone 
)
def getDB():
    return dbList[activeDB]


### RAG-Optimierung 

activeRAG = "simple"
RAGOptList = dict(
    simple="simple",
    hyde="hyde",
    multi="multi"
)
def getRAGOpt():
    return RAGOptList[activeRAG]


### PROMPTS 

# multiQuery-Prompt
multiQuery_template = """Du bist ein KI-Sprachmodell-Assistent. Deine Aufgabe ist es, fünf 
verschiedene Versionen der gegebenen Benutzerfrage zu generieren, um relevante Dokumente aus einer Vektordatenbank 
Datenbank zu finden. Ziel ist es einige der Einschränkungen der entfernungsbasierten Ähnlichkeitssuche zu überwinden,
indem du mehrere Perspektiven auf die Frage des Benutzers erzeugst.     
Gib diese alternativen Fragen durch Zeilenumbrüche getrennt aus.
Ursprüngliche Benutzerfrage: {question}"""

# HyDE-Porompt
hyde_template = """Schreibe einen Abschnitt wie er in Versicherungsbedingungen stehen könnte, um die folgende Frage zu beantworten
Frage: {question}
Abschnitt:"""

# RAG-Prompt 
promptTemplate = """
Du bist ein Assistent zur Beantwortung von Fragen im Bezug auf Versicherungsbedingungen. 
Damit du genaue Informationen geben kannst, werden dir Teile aus Dokumenten zur verfügung gestellt. 
Dafür wird die Nutzeranfrage verabeitet und eine Änlichkeitssuche in den Dokumenten gemacht. 
Diese Dokumente beinhalten die Bedingungen unterschiedlicher Produkte und unterschiedlicher Generationen. 

Teile der echten Dokumente:

{context}

---

Frage: {question}

Antworte genau und nutze dafür die Teile der Dokumente, halte dich ausreichend kurz
"""

# Test-Prompt 
testPrompt = """
Erwartete Antwort: {expected}
Wirkliche Antwort: {actual}
---
(Antworte mit 'true' oder 'false') Stimmt die wirkliche Antwort mit der erwarteten Antwort überein? 
"""

### Konfuguration bereitstellen: 

def getParameters():
    params = {
        "llm": activeLLM,
        "vectorDB": activeDB,
        "embeddingModel": activeEmbedding,
        "activeRAG": activeRAG,
        "llmOptions": list(llmList.keys()),
        "embeddingModelOptions": list(embeddingModelList.keys()),
        "vectorDBOptions": list(dbList.keys()),
        "RAGOptOptions": list(RAGOptList.keys()),

        "k": k,
        "temperature": temperature,
        "chunk_size":splitter["chunk_size"],
        "chunk_overlap":splitter["chunk_overlap"],

        "promptTemplate": promptTemplate.strip(),
        "multiQuery_template": multiQuery_template.strip(),
        "hyde_template": hyde_template.strip(),
    }
    return params

def updateParameters(params):
    global k, splitter, temperature, promptTemplate, multiQuery_template, hyde_template, activeDB, activeEmbedding, activeLLM, activeRAG, embeddingsmodel, chroma, openaiLLM
    
    activeDB = params.vectorDB
    activeLLM = params.llm
    activeEmbedding = params.embeddingModel
    activeRAG = params.activeRAG

    k = params.k
    temperature = params.temperature
    splitter["chunk_overlap"] = params.chunk_overlap
    splitter["chunk_size"] = params.chunk_size

    promptTemplate = params.promptTemplate
    multiQuery_template = params.multiQuery_template
    hyde_template = params.hyde_template

    embeddingsmodel = embeddingModelList[activeEmbedding]
    chroma = Chroma(persist_directory=dbDirectory, embedding_function=embeddingsmodel, client=chroma_client)
    openaiLLM = ChatOpenAI(model="gpt-3.5-turbo-16k", temperature=temperature)
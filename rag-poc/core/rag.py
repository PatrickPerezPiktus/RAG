import config
import argparse
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.load import dumps, loads
from langchain_core.output_parsers import  StrOutputParser
from langchain_openai import ChatOpenAI
from operator import itemgetter
from langchain_core.runnables import RunnablePassthrough

def multiQuery():
    prompt_perspectives = ChatPromptTemplate.from_template(config.multiQuery_template)

    return (prompt_perspectives | config.getLLM() | StrOutputParser() | (lambda x: x.split("\n")))

def getUniqueDocs(documents):
    flattened_docs = [dumps(doc) for sublist in documents for doc in sublist]
    unique_docs = list(set(flattened_docs))
    return [loads(doc) for doc in unique_docs]

def retrievalChain(queryInput):
    # RetrieveMulti
    retrieval_chain = multiQuery() | config.getDB().as_retriever().map() | getUniqueDocs
    docs = retrieval_chain.invoke({"question":queryInput})
    return docs


def hydeDocGeneration():
    prompt_hyde = ChatPromptTemplate.from_template(config.hyde_template)

    return (prompt_hyde | config.getLLM() | StrOutputParser())

def hydeRetrieval(queryInput): 
    hydeChain = hydeDocGeneration() | config.getDB().as_retriever()
    return hydeChain.invoke({"question":queryInput})


def queryMulti(queryInput, history): 
    results = retrievalChain(queryInput)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", config.promptTemplate),
        MessagesPlaceholder("chat_history"),
        ("human", "{question}"),
    ])

    ragChain = prompt | config.getLLM() | StrOutputParser()    

    response = ragChain.invoke({"context": results, "question": queryInput, "chat_history": history})
    sources = [doc.metadata.get("id", None) for doc in results]
    return {"response": response, "sources": sources}

def queryHyde(queryInput, history): 
    results = hydeRetrieval(queryInput)

    prompt = ChatPromptTemplate.from_messages([
        ("system", config.contextPromptTemplate),
        MessagesPlaceholder("chat_history"),
        ("human", "{question}"),
    ])

    ragChain = (prompt | config.getLLM() | StrOutputParser())

    response = ragChain.invoke({"context": results, "question": queryInput, "chat_history": history})
    sources = [doc.metadata.get("id", None) for doc in results]
    return {"response": response, "sources": sources}

def querySimple(queryInput, history):
    results = config.getDB().similarity_search_with_score(queryInput, config.k)

    prompt = ChatPromptTemplate.from_messages([
            ("system", config.promptTemplate),
            MessagesPlaceholder("chat_history"),
            ("human", "{question}"),
        ])
        
    ragChain = (prompt | config.getLLM() | StrOutputParser())

    response = ragChain.invoke({"context": results, "question": queryInput, "chat_history": history})
    sources = [doc.metadata.get("id", None) for doc, _score in results]
    return {"response": response, "sources": sources}


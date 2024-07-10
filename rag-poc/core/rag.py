import config
import argparse
from langchain.prompts import ChatPromptTemplate

from langchain.load import dumps, loads

from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from operator import itemgetter
from langchain_core.runnables import RunnablePassthrough

def multiQuery():
    prompt_perspectives = ChatPromptTemplate.from_template(config.multiQuery_template)

    return (
        prompt_perspectives 
        | config.getLLM()
        | StrOutputParser() 
        | (lambda x: x.split("\n"))
    )

def getUniqueDocs(documents):
    flattened_docs = [dumps(doc) for sublist in documents for doc in sublist]
    unique_docs = list(set(flattened_docs))
    return [loads(doc) for doc in unique_docs]

def retrievalChain(queryInput):
    # RetrieveMulti
    retrieval_chain = multiQuery() | config.getDB().as_retriever().map() | getUniqueDocs
    docs = retrieval_chain.invoke({"question":queryInput})
    len(docs)
    return docs

def queryMulti(queryInput): 
    # Retrieve
    results = retrievalChain(queryInput)
    prompt = ChatPromptTemplate.from_template(config.promptTemplate)

    ragChain = prompt | config.getLLM() | StrOutputParser()    

    response = ragChain.invoke({"context": results, "question": queryInput})
    sources = [doc.metadata.get("id", None) for doc in results]
    return {"response": response, "sources": sources}

def queryNative(queryInput):
    db = config.getDB()

    #Retrieve
    results = db.similarity_search_with_score(queryInput, config.k)
    db.as_retriever()
    
    #Augmention
    context = "\n---\n".join([doc.page_content for doc, _score in results])
    sources = [doc.metadata.get("id", None) for doc, _score in results]
    promtTemplate = ChatPromptTemplate.from_template(config.promptTemplate)
    prompt = promtTemplate.format(context=context, question=queryInput)

    #Generation
    response = config.getLLM().invoke(prompt)

    native_rag = ()

    return {"response": response, "sources": sources}
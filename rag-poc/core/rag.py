import config
import argparse
from langchain.prompts import ChatPromptTemplate

def query(queryInput):
    db = config.db

    #Retrieve
    results = db.similarity_search_with_score(queryInput, config.k)
    
    #Augmention
    context = "\n---\n".join([doc.page_content for doc, _score in results])
    sources = [doc.metadata.get("id", None) for doc, _score in results]
    promtTemplate = ChatPromptTemplate.from_template(config.promptTemplate)
    prompt = promtTemplate.format(context=context, question=queryInput)

    #Generation
    response = config.getLLM().invoke(prompt)

    return {"response": response, "sources": sources}
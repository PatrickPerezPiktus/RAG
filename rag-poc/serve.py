from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import user, chat, config, document

app = FastAPI(
    title="Wissensmanagementsystem",
    version="1.0",
    description="Prototyp eines Wissensmanagementsystem basierend auf Retrieval-Augmented-Generation",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(chat.router)
app.include_router(config.router)
app.include_router(document.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=9000)

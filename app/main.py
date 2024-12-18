import uvicorn
from sqlmodel import Session, select
from .config import create_tables, engine
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.ai.main_agent import agent
load_dotenv()


app = FastAPI(
    title="SKY ASSIST Agentic Rag Systeem",
    description="SKY ASSIST Agentic Rag Systeem to Automate the Airline",
    version="1.0.0",
)

# Set up CORS 
origins = [
    "http://localhost:3000",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)  
# Include the routers from different API modules
# app.include_router(auth.router, prefix="/auth", tags=["Auth"])
@app.get("/")
def root():
    return {"message": "SKY ASSIST Agentic Rag Systeem to Automate the Airline"}



@app.get("/chat/{query}")
def get_content(query: str):
    print(query)
    try:
        config = {"configurable": {"thread_id": "1"}}
        result = agent.invoke({"messages": [("user", query)]}, config)
        print(result)

        return result
    except Exception as e:
        return {"output": str(e)}




def start():
    # create_tables()
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
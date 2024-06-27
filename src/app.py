from dotenv import load_dotenv
from fastapi import FastAPI

from src.router.questionnaire_router import router as questionnaire_router
load_dotenv()

app = FastAPI(openapi_url="/docs/openapi.json", docs_url="/docs")

app.include_router(questionnaire_router)

@app.get("/")
async def root():
    return {"version": "0.0.2"}

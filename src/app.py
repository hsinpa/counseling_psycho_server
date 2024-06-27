from fastapi import FastAPI

app = FastAPI(openapi_url="/docs/openapi.json", docs_url="/docs")

@app.get("/")
async def root():
    return {"version": "0.0.2"}

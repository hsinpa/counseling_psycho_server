from fastapi import FastAPI

from src.utility.utility_method import chunk

app = FastAPI()
print(list(chunk([1, 2, 3, 4, 5, 6], 2)))


@app.get("/")
async def root():
    return {"Say": "Hello!"}

import requests
from fastapi import APIRouter

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])

@router.post("/chat")
async def chat():

    pass
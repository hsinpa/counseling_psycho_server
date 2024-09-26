import asyncio
from enum import Enum
from typing import Dict, Any

from google.cloud.aiplatform_v1beta1 import HarmCategory, SafetySetting
from langchain_google_vertexai import ChatVertexAI
from langchain_openai import ChatOpenAI
from openai import OpenAI

from src.service.vector_db.vector_static import TEXT_EMBEDDING_SIZE
from src.utility.static_text import OpenAI_Model_4o_mini, Gemini_Model_1_5


def get_gpt_model(model_name: str = OpenAI_Model_4o_mini, temperature: float = 0.75,
                  json_mode: bool = False, **kwargs):
    arguments = {'model': model_name, 'temperature': temperature, **kwargs}

    if json_mode is True:
        arguments['response_format'] = {"type": "json_object"}

    return ChatOpenAI(
        **arguments
    )


def get_gemini_model(model_name: str = Gemini_Model_1_5, temperature: float = 0.75,
                     json_schema: Dict[str, Any] = None, **kwargs):
    safety_settings = {
        HarmCategory.HARM_CATEGORY_UNSPECIFIED: SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH,
        HarmCategory.HARM_CATEGORY_HARASSMENT: SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    }

    arguments = {'model_name': model_name, 'temperature': temperature, 'safety_settings': safety_settings,
                 **kwargs}

    if json_schema is not None:
        arguments['response_mime_type'] = "application/json"
        arguments['response_schema'] = json_schema

    return ChatVertexAI(
        **arguments
    )

def text_embedding(corpus: list[str]):
    client = OpenAI()
    return client.embeddings.create(input=corpus, model="text-embedding-3-small", dimensions=TEXT_EMBEDDING_SIZE).data

async def atext_embedding(corpus: list[str]):
    return await asyncio.to_thread(text_embedding, corpus)

import asyncio
from enum import Enum
from typing import Dict, Any
from dotenv import load_dotenv

from google.cloud.aiplatform_v1beta1 import HarmCategory, SafetySetting
from langchain_google_vertexai import ChatVertexAI
from langchain_openai import ChatOpenAI
from openai import OpenAI
from abc import ABC, abstractmethod

from langchain_core.language_models import BaseChatModel, FakeListChatModel
from src.service.vector_db.vector_static import TEXT_EMBEDDING_SIZE
from src.utility.static_text import OpenAI_Model_4o_mini, Gemini_Model_2_0_Flash, OpenAI_Model_4o, \
    OpenAI_Model_41_mini

load_dotenv()

def get_gpt_model(model_name: str = OpenAI_Model_4o_mini, temperature: float = 0.75,
                  json_mode: bool = False, **kwargs):
    arguments = {'model': model_name, 'temperature': temperature, **kwargs}

    if json_mode is True:
        arguments['response_format'] = {"type": "json_object"}

    return ChatOpenAI(
        **arguments
    )


def get_gemini_model(model_name: str = Gemini_Model_2_0_Flash, temperature: float = 0.75,
                     json_schema: Dict[str, Any] = None, **kwargs):
    safety_settings = {
        HarmCategory.HARM_CATEGORY_UNSPECIFIED: SafetySetting.HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: SafetySetting.HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: SafetySetting.HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: SafetySetting.HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: SafetySetting.HarmBlockThreshold.BLOCK_NONE,
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

class ILLMLoader(ABC):
    @abstractmethod
    def get_llm_model(self, model_name: str, **kwargs) -> BaseChatModel:
        """Must return a string based on integer x."""
        pass


class ClassicILLMLoader(ILLMLoader):
    def __init__(self, preload=False):
        self._table = {OpenAI_Model_4o_mini: self._gpt_model,
                       OpenAI_Model_4o: self._gpt_model,
                       OpenAI_Model_41_mini: self._gpt_model,
                       Gemini_Model_2_0_Flash: self._gemini_model}
        self._preload_table = {}
        if preload:
            self._preload_table = self._preload(self._table)

    def _preload(self, lookup_table: dict):
        preload_table = {}
        for x in lookup_table:
            preload_table[x] = lookup_table[x](x)
        return preload_table

    def get_llm_model(self, model_name: str, **kwargs) -> BaseChatModel:
        # return if already loaded
        if model_name in self._preload_table:
            return self._preload_table[model_name]

        # Load model in runtime
        if model_name in self._table:
            return self._table[model_name](model_name=model_name, **kwargs)
        else:
            # Default model
            return self._gpt_model(model_name=model_name, **kwargs)

    def _gpt_model(self, model_name: str, **kwargs):
        return get_gpt_model(model_name=model_name, **kwargs)

    def _gemini_model(self, model_name: str, **kwargs):
        return get_gemini_model(model_name=model_name, **kwargs)

classic_llm_loader = ClassicILLMLoader(preload=True)

class MockLLMLoader(ILLMLoader, ABC):
    def __init__(self, fake_response: list[str]):
        self._fake_response = fake_response

    def get_llm_model(self, model_name: str, **kwargs) -> BaseChatModel:
        return FakeListChatModel(responses=self._fake_response)
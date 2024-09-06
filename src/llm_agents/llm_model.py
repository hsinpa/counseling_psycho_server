from enum import Enum
from typing import Dict, Any

from langchain_google_genai import HarmCategory, HarmBlockThreshold
from langchain_google_vertexai import ChatVertexAI
from langchain_openai import ChatOpenAI

from src.utility.static_text import OpenAI_Model_4o_mini, Gemini_Model_1_5


def get_gpt_model(model_name: str=OpenAI_Model_4o_mini, temperature: float = 0.75,
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
        HarmCategory.HARM_CATEGORY_UNSPECIFIED: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    }

    arguments = {'model_name': model_name, 'temperature': temperature, 'safety_settings': safety_settings,
                 **kwargs}

    if json_schema is not None:
        arguments['response_mime_type'] = "application/json"
        arguments['response_schema'] = json_schema

    return ChatVertexAI(
        **arguments
    )
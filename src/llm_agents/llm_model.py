from enum import Enum

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI


class LLMModel(Enum):
    Gemini = 1,
    OpenAI = 2,


def get_model(model_enum: LLMModel, **kwargs):
    if model_enum == LLMModel.Gemini:
        return ChatGoogleGenerativeAI(
            **kwargs
        )

    if model_enum == LLMModel.OpenAI:
        return ChatOpenAI(
            **kwargs
        )

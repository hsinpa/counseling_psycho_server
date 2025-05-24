import uuid
from typing import List

from langchain_core.prompts import ChatPromptTemplate
from openai.types import Embedding

from src.feature.chatbot.chatbot_agent_type import TripleType, ChatMessage, ChatbotUserEnum
from src.feature.llm_model import atext_embedding


def convert_triple_str_to_pydantic(triple_str: str) -> TripleType | None:
    try:
        s_triple = triple_str.split("|")
        triple = TripleType(
            uuid=str(uuid.uuid4()),
            host_node=s_triple[0].strip(),
            relation=s_triple[1].strip(),
            child_node=s_triple[2].strip()
        )
        return triple
    except Exception as e:
        print(f'convert_triple_str_to_pydantic error {triple_str}, {e}')
    return None


async def convert_triple_list_to_embedding(triple_list: list[TripleType]) -> list[TripleType]:
    pre_embed_texts: list[str] = list(
        map(lambda x: f'Main node: {x.host_node}, Relation: {x.relation}, Child node: {x.child_node}', triple_list))

    if len(pre_embed_texts) <= 0:
        return triple_list

    embedded_texts: list[Embedding] = await atext_embedding(pre_embed_texts)

    for triple, embedded_text in zip(triple_list, embedded_texts):
        triple.embedding = embedded_text.embedding

    return triple_list


def convert_triple_list_to_pydantic(triple_list: list[str]) -> list[TripleType]:
    triple_converts: list[TripleType] = []
    for t in triple_list:
        convert_t = convert_triple_str_to_pydantic(t)
        if convert_t is not None:
            triple_converts.append(convert_t)

    return triple_converts


def convert_triple_list_to_string(triple_list: list[TripleType], with_id: bool = False) -> str:
    triple_converts: str = ''
    for index, t in enumerate(triple_list):

        if with_id:
            triple_converts += f'[ID: {t.uuid}] '

        triple_converts += f'{t.host_node} | {t.relation} | {t.child_node}'

        if index < len(triple_list) - 1:
            triple_converts += '\n'

    return triple_converts



def db_message_to_prompt(system_prompt: str, human_prompt: str,
                         messages: list[ChatMessage]) -> ChatPromptTemplate:
    agent_message = [('system', system_prompt)]

    # Ignore narrator
    for message in messages:
        if message.message_type == ChatbotUserEnum.human:
            agent_message.extend([('human', message.body)])

        if message.message_type == ChatbotUserEnum.bot:
            agent_message.extend([('ai', message.body)])

    agent_message.append(('human', human_prompt))

    prompt_template = ChatPromptTemplate(agent_message)
    return prompt_template


import os

from dotenv import load_dotenv
from neo4j import AsyncGraphDatabase

from src.llm_agents.chatbot.chatbot_agent_type import TripleType

load_dotenv()


def get_async_neo4j_driver():
    uri = os.getenv("NEO4J_URI")
    password = os.getenv("NEO4J_PASSWORD")

    driver = AsyncGraphDatabase.driver(uri, auth=("neo4j", password))

    # async with AsyncGraphDatabase.driver(uri, auth=auth) as driver:
    return driver


def triple_to_cypher(triple_type: TripleType, user_id: str, chatbot_id: str, session_id: str):
    query = f"""\
MERGE (a_node:Node{{value: $a_value, user_id: '{user_id}', chatbot_id: '{chatbot_id}', session_id: '{session_id}' }})
MERGE (b_node:Node{{value: $b_value, user_id: '{user_id}', chatbot_id: '{chatbot_id}', session_id: '{session_id}'}})
MERGE (a_node)-[:{triple_type.relation}]->(b_node)
"""

    return query, {'a_value': triple_type.host_node, 'b_value': triple_type.child_node}

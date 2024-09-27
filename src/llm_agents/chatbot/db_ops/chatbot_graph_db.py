from src.llm_agents.chatbot.chatbot_agent_type import TripleType
from src.service.graph_db.neo4j_entry import get_async_neo4j_driver, triple_to_cypher
from src.service.graph_db.neo4j_static import MESSAGE_TRIPLE_TABLE


async def save_to_graph_db(user_id:str, session_id: str, chatbot_id: str, triple_list: list[TripleType]):
    neo4j_driver = get_async_neo4j_driver()

    async with neo4j_driver.session(database=MESSAGE_TRIPLE_TABLE) as driver:
        for triple in triple_list:
            query, q_parameter = triple_to_cypher(triple_type=triple,
                                                  user_id=user_id, session_id=session_id,
                                                  chatbot_id=chatbot_id)

            await driver.run(query=query, parameters=q_parameter)

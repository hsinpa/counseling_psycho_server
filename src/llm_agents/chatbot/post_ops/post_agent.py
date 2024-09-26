import asyncio

from qdrant_client.http.models import PointStruct

from src.llm_agents.chatbot.chatbot_agent_type import ChatbotAgentState, TripleType
from src.service.vector_db.vector_db_manager import VectorDBManager
from src.service.vector_db.vector_static import COLLECTION_CHAT


class PostAgent:
    def __init__(self, user_id: str, session_id: str, state: ChatbotAgentState, vector_db: VectorDBManager):
        self._user_id = user_id
        self._session_id = session_id
        self._state = state
        self._vector_db = vector_db
        self._new_loop = asyncio.new_event_loop()  # Create a new event loop

    def exec_pipeline(self):
        asyncio.set_event_loop(self._new_loop)
        self._new_loop.run_until_complete(self._process_post_work())

    async def _process_post_work(self):
        await self._kg_triple_to_vector_db()

    async def _kg_triple_to_vector_db(self):
        triples: list[TripleType] = self._state['kg_triples']
        points: list[PointStruct] = []

        for triple in triples:
            points.append(PointStruct(
                id=triple.uuid,
                payload={
                    'session_id': self._session_id,
                    'host_node': triple.host_node,
                    'relation': triple.relation,
                    'child_node': triple.child_node,
                },
                vector=triple.embedding
            ))

        await self._vector_db.insert(collection_name=COLLECTION_CHAT, points=points)

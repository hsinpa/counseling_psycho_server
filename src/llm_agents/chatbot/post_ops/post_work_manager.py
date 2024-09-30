import asyncio

from qdrant_client.http.models import PointStruct
from langfuse.callback import CallbackHandler

from src.llm_agents.chatbot.chatbot_agent_type import ChatbotAgentState, TripleType, ChatbotPostState
from src.llm_agents.chatbot.db_ops.chatbot_relation_db import upsert_chatroom_info, insert_chatroom_message
from src.llm_agents.chatbot.post_ops.post_agent import PostAgent
from src.service.vector_db.vector_db_manager import VectorDBManager
from src.service.vector_db.vector_static import COLLECTION_CHAT


class PostWorkManager:
    def __init__(self, user_id: str, session_id: str, state: ChatbotAgentState, vector_db: VectorDBManager):
        self._user_id = user_id
        self._session_id = session_id
        self._state = state
        self._vector_db = vector_db
        self._new_loop = asyncio.new_event_loop()  # Create a new event loop
        self._post_agent = PostAgent(user_id, session_id)
        self._compiled_agent = self._post_agent.create_graph()

    def exec_pipeline(self):
        asyncio.set_event_loop(self._new_loop)
        self._new_loop.run_until_complete(self._process_post_work())

    async def _process_post_work(self):
        insert_chatroom_message(self._session_id, self._user_id, user_message=self._state['query'],
                                agent_message=self._state['output'])

        post_data: ChatbotPostState = await self._compiled_agent.ainvoke(
            {
                **self._state
            }, config={"run_name": 'Post Graph',
               "callbacks": [CallbackHandler(
                   user_id='hsinpa',
                   session_id=self._session_id
               )]
           }
        )

        async with asyncio.TaskGroup() as tg:
            tg.create_task(self._state_to_relation_db(post_data))
            tg.create_task(self._kg_triple_to_remove_db(post_data['delete_triples']))
            tg.create_task(self._kg_triple_to_vector_db())

    async def _state_to_relation_db(self, post_data: ChatbotPostState):
        await asyncio.to_thread(upsert_chatroom_info, self._user_id, self._session_id, post_data['summary'], post_data['long_term_plan'])

    async def _kg_triple_to_remove_db(self, delete_triples: list[str]):
        await self._vector_db.delete(collection_name=COLLECTION_CHAT, point_ids=delete_triples)

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

        await self._vector_db.upsert(collection_name=COLLECTION_CHAT, points=points)
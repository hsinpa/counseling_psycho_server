from qdrant_client import models
from qdrant_client.http.models import QueryResponse

from src.feature.chatbot.chatbot_agent_type import TripleType
from src.service.vector_db.vector_db_manager import VectorDBManager
from src.service.vector_db.vector_static import COLLECTION_CHAT


async def retrieve_relate_triples(session_id: str, kg_triples: list[TripleType], vector_db: VectorDBManager) -> list[TripleType]:
    db_filter = models.Filter(
        must=[
            models.FieldCondition(
                key="session_id",
                match=models.MatchValue(
                    value=session_id,
                ),
            )
        ]
    )

    search_queries = list(map(lambda x: models.QueryRequest(query=x.embedding, filter=db_filter, limit=3, with_payload=True), kg_triples))
    qdrant_results: list[QueryResponse] = await vector_db.batch_search(collection_name=COLLECTION_CHAT, query_requests=search_queries)

    retrieve_triples: list[TripleType] = []
    for qdrant_result in qdrant_results:
        for qdrant_point in qdrant_result.points:
            # ignore score point if less than 0.5
            if qdrant_point.score < 0.5:
                continue

            retrieve_triples.append(TripleType(uuid=qdrant_point.id,
                                               host_node=qdrant_point.payload['host_node'],
                                               relation=qdrant_point.payload['relation'],
                                               child_node=qdrant_point.payload['child_node']))

    return retrieve_triples
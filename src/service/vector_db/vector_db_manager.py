import asyncio
import os

from qdrant_client import AsyncQdrantClient, models
from qdrant_client.http.models import VectorParams, Distance, PointStruct, ScalarQuantization

from src.service.vector_db.vector_static import TEXT_EMBEDDING_SIZE, COLLECTION_CHAT, COLLECTION_CHAT_INDEX_FIELD


class VectorDBManager:
    def __init__(self):
        postgres_host = os.environ['LOCALHOST']

        self._client = AsyncQdrantClient(url=f"http://{postgres_host}:6333")
        self._vectorParams = VectorParams(size=TEXT_EMBEDDING_SIZE, distance=Distance.COSINE, on_disk=True)
        self._quantization = ScalarQuantization(
            scalar=models.ScalarQuantizationConfig(
                type=models.ScalarType.INT8,
                always_ram=False,
            ),
        )

    async def init_db_collection(self):
        chat_col_status = await self._create_collection(COLLECTION_CHAT)
        if chat_col_status:
            await self._client.create_payload_index(collection_name=COLLECTION_CHAT,
                                                    field_name=COLLECTION_CHAT_INDEX_FIELD, field_schema="keyword")

    async def upsert(self, collection_name: str, points: list[PointStruct]):
        await self._client.upsert(collection_name=collection_name, points=points)

    async def search(self, collection_name: str, embedding: list[float], filters: models.Filter = None, limit=5):
        return await self._client.search(
            collection_name=collection_name,
            query_vector=embedding,
            query_filter=filters,
            limit=limit,
        )
    async def batch_search(self, collection_name: str, query_requests: list[models.QueryRequest]):
        return await self._client.query_batch_points(collection_name=collection_name, requests=query_requests, )

    async def delete(self, collection_name: str, point_ids: list[str]):
        await self._client.delete(collection_name=collection_name,
                                          points_selector=models.PointIdsList(
                                              points=point_ids,
                                          ), )

    async def _create_collection(self, collection_name: str) -> bool:
        has_collection = await self._client.collection_exists(collection_name)
        if has_collection is False:
            await self._client.create_collection(
                collection_name=collection_name,
                vectors_config=self._vectorParams,
                on_disk_payload=True,
            )
        return has_collection is False

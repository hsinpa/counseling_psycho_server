import json

from pydantic import TypeAdapter

from src.model.supervisor_model import TranscriptData, TranscriptSegment
from src.service.relation_db.postgres_db_manager import FetchType
from src.service.relation_db.sql_client_interface import SQLClientInterface
from psycopg.types.json import Jsonb

class TranscriptDBOps:
    def __init__(self, client: SQLClientInterface):
        self._table_name = 'transcript'
        self._client = client

    async def db_ops_get_transcript_info(self, session_id: str):
        sql_syntax = (f"SELECT * "
                      f"FROM {self._table_name} WHERE session_id=%s")

        result = await self._client.async_db_ops(sql_syntax=sql_syntax, fetch_type=FetchType.One, parameters=[session_id])

        if result is not None:
            segments_adapter = TypeAdapter(list[TranscriptSegment])
            segments = segments_adapter.validate_python(result['segments'])

            return TranscriptData(full_text=result['full_text'], segments=segments)

        return None

    async def db_ops_insert_transcript_info(self, session_id: str, transcript_data: TranscriptData):
        items_dict = [Jsonb(item.model_dump()) for item in transcript_data.segments]

        sql_syntax = (f"INSERT INTO {self._table_name} (session_id, full_text, segments) VALUES(%s, %s, %s::jsonb[])")

        await self._client.async_db_ops(sql_syntax=sql_syntax, fetch_type=FetchType.Idle, parameters=[session_id, transcript_data.full_text, items_dict])

    async def db_ops_update_transcript_info(self, session_id: str, transcript_data: TranscriptData):
        items_dict = [Jsonb(item.model_dump()) for item in transcript_data.segments]

        sql_syntax = f"UPDATE {self._table_name} SET full_text=%s, segments=%s::jsonb[] WHERE session_id=%s"
        await self._client.async_db_ops(sql_syntax=sql_syntax, fetch_type=FetchType.Idle,
                                        parameters=[transcript_data.full_text, items_dict, session_id])

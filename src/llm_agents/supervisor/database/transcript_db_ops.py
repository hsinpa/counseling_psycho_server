from src.service.relation_db.postgres_db_manager import FetchType
from src.service.relation_db.sql_client_interface import SQLClientInterface


class TranscriptDBOps:
    def __init__(self, client: SQLClientInterface, session_id: str):
        self._table_name = 'transcript'
        self._client = client

async def db_ops_get_transcript_info(self, session_id: str):
    sql_syntax = (f"SELECT * "
                  f"FROM {self._table_name} WHERE session_id=%s")

    result = await self.async_db_ops(sql_syntax=sql_syntax, fetch_type=FetchType.One, parameters=[session_id])

    if result is not None:
        # Rephrase theme checkbox
        print(result['segments'])

    return result


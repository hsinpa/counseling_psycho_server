import json

from pydantic import TypeAdapter

from src.feature.supervisor.supervisor_model import DB_TRANSCRIPT_TABLE, DB_SUPERVISOR_REPORT_TABLE
from src.model.supervisor_model import TranscriptData, TranscriptSegment, TranscriptDBType
from src.service.relation_db.postgres_db_manager import FetchType
from src.service.relation_db.sql_client_interface import SQLClientInterface
from psycopg.types.json import Jsonb

from src.utility.static_text import DB_TRANSCRIPT_STATUS_IN_PROGRESS


class TranscriptDBOps:
    def __init__(self, client: SQLClientInterface):
        self._client = client

    def convert_db_data_to_pydantic_type(self, raw_data: dict):
        if raw_data is not None:
            segments_adapter = TypeAdapter(list[TranscriptSegment])
            segments = segments_adapter.validate_python(raw_data['segments'])
            del raw_data['segments']

            print('convert_db_data_to_pydantic_type', raw_data)

            return TranscriptDBType(
                **raw_data,
                segments=segments
            )
        return None

    async def db_ops_get_transcript_list(self, user_id: str):
        sql_syntax = (f"SELECT DISTINCT ON (t.id) t.id, t.session_id, t.file_name, t.status, t.created_date, "
                      f"sr.status as report_status, sr.id as supervisor_report_id "
                      f"FROM {DB_TRANSCRIPT_TABLE} t "
                      f"LEFT JOIN {DB_SUPERVISOR_REPORT_TABLE} sr ON sr.transcript_id = t.id "
                      f"WHERE user_id=%s "
                      f"ORDER  BY t.id, "
                      f"CASE WHEN sr.id IS NULL THEN 1 ELSE 0 END, "
                      f"sr.id DESC")

        transcript_list = await self._client.async_db_ops(sql_syntax=sql_syntax, fetch_type=FetchType.Many, parameters=[user_id])
        transcript_list.reverse()

        return transcript_list
    async def db_ops_get_transcript_info(self, session_id: str):
        sql_syntax = (f"SELECT t.*, sr.status as report_status, sr.id as supervisor_report_id "
                      f"FROM {DB_TRANSCRIPT_TABLE} t "
                      f"LEFT JOIN {DB_SUPERVISOR_REPORT_TABLE} sr ON sr.transcript_id = t.id "
                      f"WHERE session_id=%s ORDER BY sr.id DESC")

        result = await self._client.async_db_ops(sql_syntax=sql_syntax, fetch_type=FetchType.One, parameters=[session_id])
        if result is not None:
            return self.convert_db_data_to_pydantic_type(result)

        return None

    async def db_ops_insert_transcript_info(self, session_id: str, user_id: str, file_name: str, lang_code: str,
                                            transcript_data: TranscriptData, status: str = DB_TRANSCRIPT_STATUS_IN_PROGRESS):
        items_dict = [Jsonb(item.model_dump()) for item in transcript_data.segments]

        sql_syntax = (f"INSERT INTO {DB_TRANSCRIPT_TABLE} (session_id, user_id, file_name, full_text, lang_code, status, segments) "
                      f"VALUES(%s, %s, %s, %s, %s, %s, %s::jsonb[])")

        await self._client.async_db_ops(sql_syntax=sql_syntax, fetch_type=FetchType.Idle,
                                        parameters=[session_id, user_id, file_name, transcript_data.full_text,
                                                    lang_code, status, items_dict])

    async def db_ops_update_transcript_info(self, session_id: str, transcript_data: TranscriptData, status: str):
        items_dict = [Jsonb(item.model_dump()) for item in transcript_data.segments]

        sql_syntax = f"UPDATE {DB_TRANSCRIPT_TABLE} SET full_text=%s, segments=%s::jsonb[], status=%s WHERE session_id=%s"

        await self._client.async_db_ops(sql_syntax=sql_syntax, fetch_type=FetchType.Idle,
                                        parameters=[transcript_data.full_text, items_dict, status, session_id])

    async def db_ops_update_transcript_name(self, file_name: str, session_id: str):
        sql_syntax = f"UPDATE {DB_TRANSCRIPT_TABLE} SET file_name=%s WHERE session_id=%s"
        await self._client.async_db_ops(sql_syntax=sql_syntax, fetch_type=FetchType.Idle,
                                        parameters=[file_name, session_id])

    async def db_ops_delete_transcript(self, transcript_id: int):
        del_report_syntax = f"DELETE FROM {DB_SUPERVISOR_REPORT_TABLE} WHERE transcript_id=%s"
        del_transcript_syntax = f"DELETE FROM {DB_TRANSCRIPT_TABLE} WHERE id=%s"

        await self._client.async_db_ops(sql_syntax=del_report_syntax, fetch_type=FetchType.Idle, parameters=[transcript_id])
        await self._client.async_db_ops(sql_syntax=del_transcript_syntax, fetch_type=FetchType.Idle, parameters=[transcript_id])

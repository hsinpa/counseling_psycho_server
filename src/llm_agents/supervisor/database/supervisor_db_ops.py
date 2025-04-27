import json

from pydantic import TypeAdapter

from src.llm_agents.supervisor.supervisor_model import SupervisorAnalysisRespModel, DB_SUPERVISOR_REPORT_TABLE, DB_TRANSCRIPT_TABLE
from src.model.supervisor_model import TranscriptData, TranscriptSegment
from src.service.relation_db.postgres_db_manager import FetchType
from src.service.relation_db.sql_client_interface import SQLClientInterface
from psycopg.types.json import Jsonb

from src.utility.static_text import DB_TRANSCRIPT_STATUS_COMPLETE


class SupervisorReportDBOps:
    def __init__(self, client: SQLClientInterface):
        self._client = client

    async def db_ops_get_supervisor_report(self, session_id: str):
        sql_syntax = (f"SELECT sr.* FROM {DB_SUPERVISOR_REPORT_TABLE} sr "
                      f"JOIN {DB_TRANSCRIPT_TABLE} t ON sr.transcript_id = t.id "
                      f"WHERE t.session_id=%s "
                      f"ORDER BY sr.created_date DESC LIMIT 1")

        return await self._client.async_db_ops(sql_syntax=sql_syntax, fetch_type=FetchType.One,
                                        parameters=[session_id])

    async def db_ops_insert_supervisor_report(self, transcript_id: str,
                                              analysis_data: SupervisorAnalysisRespModel):

        case_concept_dict = Jsonb(analysis_data.case_conceptualization.model_dump())
        homework_dict = Jsonb(analysis_data.homework_assignment.model_dump())
        issue_treatments_array = [Jsonb(item.model_dump()) for item in analysis_data.issue_treatment_strategies]

        sql_syntax = (f"INSERT INTO {DB_SUPERVISOR_REPORT_TABLE} "
                      f"(transcript_id, case_conceptualization, homework_assignment, issue_treatment_strategies, status) "
                      f"VALUES(%s, %s::jsonb, %s::jsonb, %s::jsonb[], %s)")
        await self._client.async_db_ops(sql_syntax=sql_syntax, fetch_type=FetchType.Idle,
                                        parameters=[transcript_id, case_concept_dict, homework_dict, issue_treatments_array,
                                                    DB_TRANSCRIPT_STATUS_COMPLETE])


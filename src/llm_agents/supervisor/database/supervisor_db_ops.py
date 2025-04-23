import json

from pydantic import TypeAdapter

from src.llm_agents.supervisor.supervisor_model import SupervisorAnalysisRespModel
from src.model.supervisor_model import TranscriptData, TranscriptSegment
from src.service.relation_db.postgres_db_manager import FetchType
from src.service.relation_db.sql_client_interface import SQLClientInterface
from psycopg.types.json import Jsonb

class SupervisorReportDBOps:
    def __init__(self, client: SQLClientInterface):
        self._table_name = 'supervisor_report'
        self._client = client

    async def db_ops_insert_supervisor_report(self, session_id: str,
                                              analysis_data: SupervisorAnalysisRespModel):

        case_concept_dict = Jsonb(analysis_data.case_conceptualization.model_dump())
        homework_dict = Jsonb(analysis_data.homework_assignment.model_dump())
        issue_treatments_array = [Jsonb(item.model_dump()) for item in analysis_data.issue_treatment_strategies]

        sql_syntax = (f"INSERT INTO {self._table_name} "
                      f"(session_id, case_conceptualization, homework_assignment, issue_treatment_strategies) "
                      f"VALUES(%s, %s::jsonb, %s::jsonb, %s::jsonb[])")
        await self._client.async_db_ops(sql_syntax=sql_syntax, fetch_type=FetchType.Idle,
                                        parameters=[session_id, case_concept_dict, homework_dict, issue_treatments_array])


import json

from src.llm_agents.talk_simulation.talk_simulation_type import QuestionType
from src.model.talk_simulation_model import SimulationQuesUserInputType, GLOBAL_SIMULATION_CHECKBOX_DICT
from src.service.relation_db.postgres_db_manager import sync_db_ops, FetchType, async_db_ops
from src.service.relation_db.postgresql_db_client import PostgreSQLClient
from src.service.relation_db.sql_client_interface import SQLClientInterface
from src.utility.utility_method import clamp

TABLE = 'talk_simulation'

def db_ops_get_simulation_info(client: SQLClientInterface, session_id: str):
    """ Should be used by internal functions only, do not exposed """
    sql_syntax = (f"SELECT * "
                  f"FROM {TABLE} WHERE session_id=%s")

    result = client.sync_db_ops(sql_syntax=sql_syntax, fetch_type=FetchType.One, parameters=[session_id])

    if result is not None:
        # Rephrase theme checkbox
        theme_checkboxes = list(map(lambda x: GLOBAL_SIMULATION_CHECKBOX_DICT[x], result['theme_checkboxes']))
        result['theme_checkboxes'] = theme_checkboxes

    return result

def db_ops_get_simulation_external_view(client: SQLClientInterface, session_id: str):
    """ Information grab by external API"""
    sql_syntax = (f"SELECT id, report, questionnaires, array_length(questionnaires, 1) as process_count, report_flag "
                  f"FROM {TABLE} WHERE session_id=%s")

    result = client.sync_db_ops(sql_syntax=sql_syntax, fetch_type=FetchType.One, parameters=[session_id])

    # Rephrase questionnaire
    questionnaire_len = len(result['questionnaires'])
    result['questionnaires'] = result['questionnaires'][questionnaire_len - 1]

    return result

def db_ops_save_basic_info(user_input: SimulationQuesUserInputType):
    sql_exist = f'''SELECT id FROM {TABLE} WHERE session_id = %s'''
    exist_result = sync_db_ops(sql_syntax=sql_exist, fetch_type=FetchType.One, parameters=[user_input.session_id])

    if exist_result is not None:
        return

    checkboxes = list(map(lambda x: x.id, user_input.theme_checkboxes))
    sql_insert = f'''INSERT INTO {TABLE} (session_id, age, gender, job, education, theme_checkboxes, theme_reason, sorting_reason) 
    VALUES(%s, %s, %s, %s,   %s, %s, %s, %s )'''
    sync_db_ops(sql_syntax=sql_insert,
                parameters=[user_input.session_id, user_input.age, user_input.gender, user_input.job,
                            user_input.education, checkboxes, user_input.theme_reason, user_input.sorting_reason])


async def db_ops_save_gen_questionnaire(session_id: str, questionnaires: list[QuestionType], process_count_flag: bool = False):
    items_dict = [item.model_dump() for item in questionnaires]
    json_string = json.dumps(items_dict, indent=4, ensure_ascii=False)

    if process_count_flag is False:
        fetch_sql_syntax = (f"SELECT questionnaires FROM {TABLE} WHERE session_id=%s")
        fetch_result = await async_db_ops(sql_syntax=fetch_sql_syntax, fetch_type=FetchType.One, parameters=[session_id])

        if fetch_result is None:
            return

        questionnaires_len = len(fetch_result['questionnaires'])
        questionnaires_index = clamp(questionnaires_len - 1, 0, questionnaires_len)
        previous_json_row =  json.dumps(fetch_result['questionnaires'][questionnaires_index], indent=4, ensure_ascii=False)

        update_sql_syntax = f"""UPDATE {TABLE} SET questionnaires = array_replace(questionnaires, %s::jsonb, %s::jsonb), 
        report_flag=TRUE WHERE session_id=%s"""

        sync_db_ops(sql_syntax=update_sql_syntax,
                    parameters=[previous_json_row, json_string, session_id])
    else:
        update_sql_syntax = f"""UPDATE {TABLE} SET questionnaires=array_append(questionnaires, %s), 
        report_flag=TRUE WHERE session_id=%s"""

        sync_db_ops(sql_syntax=update_sql_syntax,
                    parameters=[json_string, session_id])

def db_ops_save_output_report(session_id: str, report: str):
    sql_syntax = f"UPDATE {TABLE} SET report=%s, report_flag=FALSE WHERE session_id=%s"

    sync_db_ops(sql_syntax=sql_syntax,
                parameters=[report, session_id])
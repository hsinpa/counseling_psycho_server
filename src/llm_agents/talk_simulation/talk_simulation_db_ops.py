import json

from src.llm_agents.talk_simulation.talk_simulation_type import QuestionType
from src.model.talk_simulation_model import SimulationQuesUserInputType
from src.service.relation_db.postgres_db_manager import sync_db_ops, FetchType

TABLE = 'talk_simulation'

def db_ops_get_simulation_info(session_id: str):
    sql_syntax = (f"SELECT id, process_count, report, questionnaires "
                  f"FROM {TABLE} WHERE session_id=%s")

    result = sync_db_ops(sql_syntax=sql_syntax, fetch_type=FetchType.One, parameters=[session_id])
    print(result)
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


def db_ops_save_gen_questionnaire(session_id: str, questionnaires: list[QuestionType] ):
    items_dict = [item.model_dump() for item in questionnaires]
    json_string = json.dumps(items_dict, indent=4, ensure_ascii=False)

    sql_syntax = f"UPDATE {TABLE} SET questionnaires=%s, process_count=process_count + 1 WHERE session_id=%s"

    sync_db_ops(sql_syntax=sql_syntax,
                parameters=[json_string, session_id])
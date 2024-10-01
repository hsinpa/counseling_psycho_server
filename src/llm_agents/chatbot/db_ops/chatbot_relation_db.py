import uuid
from typing import List

from pydantic import TypeAdapter

from src.llm_agents.chatbot.chatbot_agent_type import ChatroomInfo, ChatbotUserEnum, ChatMessage
from src.service.relation_db.postgres_db_manager import async_db_ops, FetchType, sync_db_ops
from src.service.relation_db.postgres_db_static import DB_TABLE_CHATROOM, DB_TABLE_MESSAGES


def get_chatroom_info(session_id: str):
    sql_syntax = f"""SELECT id, summary, long_term_plan, created_date 
    FROM {DB_TABLE_CHATROOM} WHERE session_id = %s"""

    sql_result = sync_db_ops(sql_syntax=sql_syntax, fetch_type=FetchType.One, parameters=[session_id])

    if sql_result is not None:
        return  ChatroomInfo(**sql_result)

    return ChatroomInfo()


def upsert_chatroom_info(user_id: str, session_id: str, summary: str, long_term_plan: str):
    fetch_result = get_chatroom_info(session_id)

    # Insert
    if fetch_result.id == '':
        sql_syntax = f"""INSERT INTO {DB_TABLE_CHATROOM} (user_id, session_id, summary, long_term_plan) VALUES(%s, %s, %s, %s)"""
        sync_db_ops(sql_syntax=sql_syntax,
                                 parameters=[user_id, session_id, summary, long_term_plan])
        return

    # Update
    sql_syntax = f"UPDATE {DB_TABLE_CHATROOM} SET summary=%s, long_term_plan=%s WHERE session_id=%s"
    sql_result = sync_db_ops(sql_syntax=sql_syntax,  parameters=[summary, long_term_plan, session_id])

def get_chatroom_message(user_id: str, session_id: str, limit: int):
    sql_syntax = f"""SELECT * FROM {DB_TABLE_MESSAGES} WHERE user_id = %s AND session_id = %s LIMIT %s"""

    sql_result = sync_db_ops(sql_syntax=sql_syntax, fetch_type=FetchType.Many, parameters=[user_id, session_id, limit])
    ta = TypeAdapter(List[ChatMessage])

    return ta.validate_python(sql_result)

def insert_chatroom_message(session_id: str, user_id: str, user_message: str, agent_message: str):
    sql_syntax = f"""INSERT INTO {DB_TABLE_MESSAGES} (user_id, session_id, bubble_id, message_type, body) 
     VALUES (%s, %s, %s, %s, %s), (%s, %s, %s, %s, %s)"""

    sql_result = sync_db_ops(sql_syntax=sql_syntax,
                             parameters=[user_id, session_id, str(uuid.uuid4()), ChatbotUserEnum.human, user_message,
                                         user_id, session_id, str(uuid.uuid4()), ChatbotUserEnum.bot, agent_message])
import os

from langfuse.callback import CallbackHandler
from typing import List
from dotenv import load_dotenv

load_dotenv()

def get_langfuse_callback(session_id: str = None, tags: List[str] = []) -> CallbackHandler:
    langfuse_handler = CallbackHandler(
        user_id=os.environ.get('LANGFUSE_USER_ID'),
        host=os.environ.get('LANGFUSE_HOST'),
        public_key=os.environ.get('LANGFUSE_PUBLIC_KEY'),
        secret_key=os.environ.get('LANGFUSE_SECRET_KEY'),
    )

    if session_id is not None:
        langfuse_handler.session_id = session_id

    if tags:
        langfuse_handler.tags = tags

    return langfuse_handler
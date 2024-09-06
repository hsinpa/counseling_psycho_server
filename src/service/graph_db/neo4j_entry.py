import os

from dotenv import load_dotenv
from neo4j import AsyncGraphDatabase

load_dotenv()

def get_async_neo4j_driver():
    uri = os.getenv("NEO4J_URI")
    password = os.getenv("NEO4J_PASSWORD")

    driver = AsyncGraphDatabase.driver(uri, auth=("neo4j", password))

    # async with AsyncGraphDatabase.driver(uri, auth=auth) as driver:
    return driver
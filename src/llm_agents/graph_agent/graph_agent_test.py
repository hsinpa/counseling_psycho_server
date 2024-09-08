import json

from src.model.cypher_model import CypherGraph, LLMCypherType


def test_graph_schema():
    schema = LLMCypherType.model_json_schema()
    print(schema)  # (2)!


if __name__ == '__main__':
    test_graph_schema()
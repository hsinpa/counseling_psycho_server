from enum import Enum

from pydantic import BaseModel, Field


class RelationEnum(str, Enum):
    Directed = 'directed'
    Bidirected = 'bidirected'


class CypherNode(BaseModel):
    label: str = Field(..., description='describe the type or a label of a node')
    property_key: str = Field(..., description='What is the type or tag of property')
    property_value: str = Field(..., description='The actual value')


class CypherRelation(BaseModel):
    label: str
    relation: RelationEnum


class CypherGraph(BaseModel):
    node_1: CypherNode
    relation: CypherRelation
    node_2: CypherNode


class LLMCypherType(BaseModel):
    thought: str = Field(...,
                         description='The thought process and your analysis, on how the knowledge should be conduct')
    knowledge_graph: list[CypherGraph] = Field(..., description='Array of knowledge graph nodes')
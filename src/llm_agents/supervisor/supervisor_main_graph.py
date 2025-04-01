from langgraph.graph.graph import CompiledGraph

from src.llm_agents.agent_interface import GraphAgent
from src.llm_agents.llm_model import ILLMLoader


class SupervisorGraph(GraphAgent):

    def __init__(self, llm_loader: ILLMLoader):
        self._llm_loader = llm_loader


    def create_graph(self) -> CompiledGraph:
        pass
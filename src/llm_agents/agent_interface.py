from abc import ABC, abstractmethod

from langgraph.graph.graph import CompiledGraph


class GraphAgent(ABC):

    @abstractmethod
    def create_graph(self) -> CompiledGraph:
        pass
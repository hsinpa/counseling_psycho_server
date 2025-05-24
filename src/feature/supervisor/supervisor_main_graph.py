from langgraph.graph.graph import CompiledGraph
from langgraph.constants import END
from langgraph.graph import StateGraph
from src.feature.agent_interface import GraphAgent
from src.feature.llm_model import ILLMLoader
from src.feature.supervisor.homework.homework_graph import HomeworkGraph
from src.feature.supervisor.case_treatment.case_treatment_graph import CaseTreatmentGraph
from src.feature.supervisor.prerequisite.prerequisite_graph import PrerequisiteGraph
from src.feature.supervisor.strategy.strategy_graph import StrategyGraph
from src.feature.supervisor.supervisor_main_state import SupervisorMainState


class SupervisorGraph(GraphAgent):

    def __init__(self, llm_loader: ILLMLoader):
        self._llm_loader = llm_loader

    async def _prerequisite_node(self, state: SupervisorMainState):
        prerequisite_graph = PrerequisiteGraph(llm_loader=self._llm_loader)
        graph = prerequisite_graph.create_graph()

        graph_result = await graph.ainvoke(
            {'transcribe_text': state['transcribe_text']},
            {
                "run_name": "Prerequisite Graph",
            },
        )

        return {'prerequisite': graph_result}

    async def _strategy_node(self, state: SupervisorMainState):
        strategy_graph = StrategyGraph(llm_loader=self._llm_loader)
        graph = strategy_graph.create_graph()

        graph_result = await graph.ainvoke(
            {
                'transcribe_text': state['transcribe_text'],
                'therapy_issue_objective': state['prerequisite']['therapy_issue_objective'],
             },
            {
                "run_name": "Strategy Graph",
            },
        )

        return {'strategy': graph_result}

    async def _case_treatment_node(self, state: SupervisorMainState):
        case_treatment_graph = CaseTreatmentGraph(llm_loader=self._llm_loader)
        graph = case_treatment_graph.create_graph()

        graph_result = await graph.ainvoke(
            {
                "transcribe_text": state["transcribe_text"],
                "treatment_framework": state["prerequisite"]["treatment_framework"],
                "therapy_issue_objective": state["prerequisite"]["therapy_issue_objective"],
                "knowledge_graph_issue": state["strategy"]["knowledge_graph_issue"],
            },
            {
                "run_name": "Case Treatment Graph",
            },
        )

        return {'case_treatment': graph_result}

    async def _homework_node(self, state: SupervisorMainState):
        homework_graph = HomeworkGraph(llm_loader=self._llm_loader)
        graph = homework_graph.create_graph()

        graph_result = await graph.ainvoke(
            {'transcribe_text': state['transcribe_text'],
                'therapy_issue_objective': state['prerequisite']['therapy_issue_objective'],
                'knowledge_graph_issue': state['strategy']['knowledge_graph_issue'],
             },
            {
                "run_name": "Homework Graph",
            },
        )

        return {'homework_assignment': graph_result}

    def create_graph(self) -> CompiledGraph:
        g_workflow = StateGraph(SupervisorMainState)

        g_workflow.add_node('prerequisite_node', self._prerequisite_node)
        g_workflow.add_node('strategy_graph', self._strategy_node)
        g_workflow.add_node('case_treatment_graph', self._case_treatment_node)
        g_workflow.add_node('homework_graph', self._homework_node)

        g_workflow.set_entry_point('prerequisite_node')

        g_workflow.add_edge('prerequisite_node', 'strategy_graph')
        g_workflow.add_edge('strategy_graph', 'case_treatment_graph')
        g_workflow.add_edge('strategy_graph', 'homework_graph')
        g_workflow.add_edge('homework_graph', END)

        return g_workflow.compile()
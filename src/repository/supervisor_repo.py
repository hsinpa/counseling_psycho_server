from typing import List

from src.llm_agents.llm_model import ILLMLoader
from src.llm_agents.supervisor.case_concept_model import CaseConceptualizationModel, CoreIntermediateBelief, \
    RelevantHistoryPrecipitant, MeanOfAT, SingleCognitiveModel, CopingStrategy
from src.llm_agents.supervisor.supervisor_main_graph import SupervisorGraph
from src.llm_agents.supervisor.supervisor_main_state import SupervisorMainState
from src.utility.langfuse_helper import get_langfuse_callback
from src.utility.utility_method import parse_json
from pydantic import TypeAdapter

class SupervisorRepo:
    def __init__(self, llm_loader: ILLMLoader):
        self._llm_loader = llm_loader

    def _post_process_analysis_report(self, state: SupervisorMainState) -> CaseConceptualizationModel:
        core_intermediate_belief_json = parse_json(state['strategy']['core_intermediate_belief'])
        core_intermediate_belief = CoreIntermediateBelief(**core_intermediate_belief_json)

        relevant_history_precipitants_json = parse_json(state['strategy']['relevant_history_precipitants'])
        relevant_history_precipitants = RelevantHistoryPrecipitant(**relevant_history_precipitants_json)

        mean_of_AT_json = parse_json(state['strategy']['mean_of_AT'])
        mean_of_AT_adapter = TypeAdapter(List[MeanOfAT])
        mean_of_AT = mean_of_AT_adapter.validate_python(mean_of_AT_json)

        cognitive_model_json = parse_json(state['strategy']['cognitive_model'])
        cognitive_model_adapter = TypeAdapter(List[SingleCognitiveModel])
        cognitive_models = cognitive_model_adapter.validate_python(cognitive_model_json)

        coping_strategy_json = parse_json(state['strategy']['coping_strategy'])
        coping_strategy = CopingStrategy(**coping_strategy_json)

        return CaseConceptualizationModel(
            core_intermediate_belief=core_intermediate_belief,
            relevant_history_precipitants=relevant_history_precipitants,
            mean_of_AT=mean_of_AT,
            cognitive_model=cognitive_models,
            coping_strategy=coping_strategy,
        )


    async def generate_analysis_report(self, transcribe_text: str):
        supervisor_graph = SupervisorGraph(llm_loader=self._llm_loader)
        graph = supervisor_graph.create_graph()

        graph_result = await graph.ainvoke(
            {'transcribe_text': transcribe_text},
            {
                "run_name": "Supervisor Full Graph",
                "callbacks": [get_langfuse_callback()],
            },
        )

        return self._post_process_analysis_report(graph_result)



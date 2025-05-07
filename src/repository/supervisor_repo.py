from typing import List

from src.llm_agents.llm_model import ILLMLoader
from src.llm_agents.supervisor.supervisor_model import CaseConceptualizationModel, CoreIntermediateBelief, \
    RelevantHistoryPrecipitant, MeanOfAT, SingleCognitiveModel, CopingStrategy, SupervisorAnalysisRespModel, \
    HomeworkAssignment, IssueTreatmentStrategy, TreatmentStep, TreatmentEvaluation
from src.llm_agents.supervisor.supervisor_main_graph import SupervisorGraph
from src.llm_agents.supervisor.supervisor_main_state import SupervisorMainState
from src.utility.langfuse_helper import get_langfuse_callback
from src.utility.utility_method import parse_json
from pydantic import TypeAdapter


def parse_therapy_issue_name(input_string: str):
    # Split the string by the colon
    parts = input_string.split(":", 1)

    if len(parts) == 2:
        prefix = parts[0].strip()  # This is the "T1-T3" part
        text = parts[1].strip()  # This is the "Emotional Distress" part

        # Parse the prefix to extract the range endpoints
        if "-" in prefix:
            start, end = prefix.split("-", 1)
            return text, [start, end]
        else:
            # If there's no range, just return the prefix in an array
            return text, [prefix]
    else:
        # Handle case where there's no colon
        return input_string, []


class SupervisorRepo:
    def __init__(self, llm_loader: ILLMLoader):
        self._llm_loader = llm_loader

    def _post_process_case_conceptualization(self, state: SupervisorMainState) -> CaseConceptualizationModel:
        core_intermediate_belief_json = parse_json(state['strategy']['core_intermediate_belief'])
        core_intermediate_belief = CoreIntermediateBelief(**core_intermediate_belief_json)

        relevant_history_precipitants_json = parse_json(state['strategy']['relevant_history_precipitants'])
        relevant_history_precipitants = RelevantHistoryPrecipitant(**relevant_history_precipitants_json)

        mean_of_AT_json = parse_json(state['strategy']['meaning_of_AT'])
        mean_of_AT_adapter = TypeAdapter(List[MeanOfAT])
        mean_of_AT = mean_of_AT_adapter.validate_python(mean_of_AT_json['situations'])

        cognitive_model_json = parse_json(state['strategy']['cognitive_model'])
        cognitive_model_adapter = TypeAdapter(List[SingleCognitiveModel])
        cognitive_models = cognitive_model_adapter.validate_python(cognitive_model_json['cognitive_model'])

        coping_strategy_json = parse_json(state['strategy']['coping_strategy'])
        coping_strategy = CopingStrategy(**coping_strategy_json)

        return CaseConceptualizationModel(
            core_intermediate_belief=core_intermediate_belief,
            relevant_history_precipitants=relevant_history_precipitants,
            meaning_of_AT=mean_of_AT,
            cognitive_model=cognitive_models,
            coping_strategy=coping_strategy,
        )

    def _post_process_homework(self, state: SupervisorMainState) -> HomeworkAssignment:
        homework_assignment_json = parse_json(state['homework_assignment']['homework_assignment'])
        return HomeworkAssignment(**homework_assignment_json)

    def _post_issue_treament_strategy(self, state: SupervisorMainState) -> List[IssueTreatmentStrategy]:
        issue_treatment_strategies: List[IssueTreatmentStrategy] = []

        treatment_strategy_raw = parse_json(state['case_treatment']['case_treatment_strategy'])
        treatment_evaluation_raw = parse_json(state['case_treatment']['case_phase_evaluation_criteria'])

        for treatment_strategy_json, treatment_evaluation_json  in zip(treatment_strategy_raw['issue'],
                                                        treatment_evaluation_raw['issue']):
            issue_name = treatment_strategy_json['issue']
            goal = treatment_strategy_json['goal']
            focus_of_stepped_care = treatment_strategy_json['focus_of_stepped_care']

            treatment_step_adapter = TypeAdapter(List[TreatmentStep])
            treatment_steps = treatment_step_adapter.validate_python(treatment_strategy_json['steps'])

            treatment_evaluation_adapter = TypeAdapter(List[TreatmentEvaluation])
            treatment_evaluations = treatment_evaluation_adapter.validate_python(treatment_evaluation_json['steps'])

            issue_treatment_strategies.append(
                IssueTreatmentStrategy(
                    treatment_evaluations=treatment_evaluations,
                    treatment_steps=treatment_steps,
                    issue= issue_name,
                    goal= goal,
                    focus_of_stepped_care=focus_of_stepped_care,
                )
            )

        return issue_treatment_strategies


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

        analysis_resp = SupervisorAnalysisRespModel(
            case_conceptualization=self._post_process_case_conceptualization(graph_result),
            homework_assignment=self._post_process_homework(graph_result),
            issue_treatment_strategies=self._post_issue_treament_strategy(graph_result)
        )

        return analysis_resp



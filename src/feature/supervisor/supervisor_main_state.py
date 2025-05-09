from typing import TypedDict

from src.feature.supervisor.homework.homework_state import HomeworkState
from src.feature.supervisor.case_treatment.case_treatment_state import CaseTreatmentState
from src.feature.supervisor.strategy.strategy_state import StrategyState
from src.feature.supervisor.prerequisite.prerequisite_state import PrerequisiteState


class SupervisorMainState(TypedDict):
    transcribe_text: str
    prerequisite: PrerequisiteState
    case_treatment: CaseTreatmentState
    strategy: StrategyState
    homework_assignment: HomeworkState
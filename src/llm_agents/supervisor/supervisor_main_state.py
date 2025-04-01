from typing import TypedDict

from src.llm_agents.supervisor.homework.homework_state import HomeworkState
from src.llm_agents.supervisor.prerequisite.prerequisite_state import PrerequisiteState
from src.llm_agents.supervisor.strategy.strategy_state import StrategyState


class SupervisorMainState(TypedDict):
    transcribe_text: str
    pre_requisites: PrerequisiteState
    strategy: StrategyState
    homework_assignment: HomeworkState
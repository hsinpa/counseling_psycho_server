import json

import pytest

from src.llm_agents.llm_model import classic_llm_loader
from src.llm_agents.supervisor.supervisor_main_graph import SupervisorGraph
from src.repository.supervisor_repo import SupervisorRepo
from src.utility.langfuse_helper import get_langfuse_callback


@pytest.mark.asyncio
async def test_supervisor_requisite_plan():
    # Arrange
    with open("./assets/text/mock/mock_conversation_2.txt", encoding='utf-8') as f:
        mock_data: str = f.read()

    supervisor_graph = SupervisorGraph(llm_loader=classic_llm_loader)
    graph = supervisor_graph.create_graph()

    graph_result = await graph.ainvoke(
        {"transcribe_text": mock_data},
        {
            "run_name": "Test Supervisor Full Graph",
            "callbacks": [get_langfuse_callback()],
        },
    )

@pytest.mark.asyncio
async def test_supervisor_requisite_model():
    # Arrange
    with open("./assets/text/mock/mock_analysis_1.json", encoding='utf-8') as f:
        mock_data: str = f.read()

    json_object = json.loads(mock_data)

    supervisor_repo = SupervisorRepo(llm_loader=classic_llm_loader)

    homework = supervisor_repo._post_process_homework(json_object)
    case_conceptualization = supervisor_repo._post_process_case_conceptualization(json_object)
    treatments = supervisor_repo._post_issue_treament_strategy(json_object)

    print(treatments)
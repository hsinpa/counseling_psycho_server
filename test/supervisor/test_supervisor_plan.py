import pytest

from src.llm_agents.llm_model import classic_llm_loader
from src.llm_agents.supervisor.prerequisite.prerequisite_graph import PrerequisiteGraph
from src.llm_agents.supervisor.supervisor_main_graph import SupervisorGraph
from src.utility.langfuse_helper import get_langfuse_callback


# @pytest.mark.asyncio
# async def test_supervisor_requisite_plan():
#     # Arrange
#     with open("./assets/text/mock/mock_conversation_1.txt", encoding='utf-8') as f:
#         mock_data: str = f.read()
#
#     prerequisite_graph = PrerequisiteGraph(llm_loader=classic_llm_loader)
#     graph = prerequisite_graph.create_graph()
#
#     graph_result = await graph.ainvoke(
#         {'transcribe_text': mock_data},
#         {
#             "run_name": "Supervisor Prerequisite",
#             "callbacks": [get_langfuse_callback()],
#         },
#     )

@pytest.mark.asyncio
async def test_supervisor_plan():
    # Arrange
    with open("./assets/text/mock/mock_conversation_1.txt", encoding='utf-8') as f:
        mock_data: str = f.read()

    supervisor_graph = SupervisorGraph(llm_loader=classic_llm_loader)
    graph = supervisor_graph.create_graph()

    graph_result = await graph.ainvoke(
        {'transcribe_text': mock_data},
        {
            "run_name": "Supervisor Full Graph",
            "callbacks": [get_langfuse_callback()],
        },
    )

    print('pre_requisites', graph_result['pre_requisites'])
    print('strategy', graph_result['strategy'])
    print('homework_assignment', graph_result['homework_assignment'])
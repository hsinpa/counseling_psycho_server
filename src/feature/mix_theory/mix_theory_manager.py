from langgraph.graph.graph import CompiledGraph

from src.feature.mix_theory.mix_theory_agent import MixTheoryAgent
from src.model.multi_theory_model import MixTheoryInputType, MultiTheoryDataType
from src.utility.theory_utility import GLOBAL_PSYCHO_THEORY_ARRAY
from langfuse.callback import CallbackHandler


class MixTheoryManager:
    def __init__(self, user_input: MixTheoryInputType):
        self._user_input = user_input

    async def execute_pipeline(self, token_ids: list[str]):
        selected_questionnaire_list: list[MultiTheoryDataType] = []
        for index, theory in enumerate(GLOBAL_PSYCHO_THEORY_ARRAY.theory):
            if theory.id in self._user_input.theory_id:
                selected_questionnaire_list.append(theory)

        agent = MixTheoryAgent(socket_id=self._user_input.user_id, token_ids=token_ids)
        compiled_graph: CompiledGraph = agent.compile_graph()

        r = await compiled_graph.ainvoke({
            'selected_theory_list': selected_questionnaire_list,
            'user_info': self._user_input.content
        },
            config={"run_name": 'MIX_Theory_Report',
                    "callbacks": [CallbackHandler()]
            }
        )

        return r
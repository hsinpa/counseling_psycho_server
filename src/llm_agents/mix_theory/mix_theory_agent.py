from langgraph.graph import StateGraph

from src.llm_agents.mix_theory.mix_theory_type import MixTheoryGraphState
from src.llm_agents.share_component.theory_components import select_theory_chain


class MixTheoryAgent:

    async def _select_theory_chain(self, state: MixTheoryGraphState):
        selected_questionnaire_list = await select_theory_chain(
            basic_info=state['user_info'],
            questionnaire_full_text=state['questionnaire_full_text']
        )

        return {'selected_questionnaire_list': selected_questionnaire_list}


    async def compile_graph(self):
        g_workflow = StateGraph(MixTheoryGraphState)

        g_workflow.add_node('select_theories', self._select_theory_chain)
        g_workflow.add_node('output_report', self._output_report_chain)

        g_workflow.set_entry_point('select_theories')
        g_workflow.add_edge('select_theories', 'output_report')
        g_workflow.add_edge('output_report', END)

        g_compile = g_workflow.compile()

        return g_compile


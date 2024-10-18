from langchain_core.output_parsers import StrOutputParser

from src.llm_agents.llm_model import get_gpt_model, get_gemini_model
from src.llm_agents.prompt.multi_theory_prompt import MIX_THEORY_CREATION_PROMPT, MULTI_THEORY_CREATION_PROMPT
from src.model.general_model import SocketEvent
from src.model.multi_theory_model import MixTheoryInputType, MultiTheoryInputType, MultiTheoryDataType
from src.model.questionnaire_model import QuestionnaireRespType
from src.types.router_input_type import InputMediaStrategyType, AnalysisInputQuestionnairesType
from src.utility.simple_prompt_factory import SimplePromptFactory
from src.utility.simple_prompt_streamer import SimplePromptStreamer
from src.utility.static_text import Gemini_Model_1_5
from src.utility.theory_utility import psycho_theory_dict, GLOBAL_PSYCHO_THEORY_ARRAY
from src.utility.utility_method import group_user_persoanl_info, group_user_input_theory_quiz


async def output_individual_strategy(user_input: InputMediaStrategyType, prompt_template: str):
    simple_streamer = SimplePromptStreamer(socket_id=user_input.user_id, session_id=user_input.session_id,
                                           event_tag=SocketEvent.bot)

    factory = SimplePromptFactory(llm_model=get_gpt_model())

    chain = factory.create_chain(output_parser=StrOutputParser(),
                                 human_prompt_text=prompt_template,
                                 partial_variables={'content': user_input.content})

    result = await simple_streamer.execute(chain=chain)

    return QuestionnaireRespType(id=user_input.session_id, content=result)


async def output_theory_report(analysis_input: AnalysisInputQuestionnairesType, prompt_template: str):
    user_personal_info = group_user_persoanl_info(analysis_input.user_meta)
    user_theory_report = group_user_input_theory_quiz(analysis_input.question_answer_pairs)

    simple_streamer = SimplePromptStreamer(socket_id=analysis_input.user_id, session_id=analysis_input.session_id,
                                           event_tag=SocketEvent.bot)
    factory = SimplePromptFactory(llm_model=get_gpt_model())

    chain = factory.create_chain(output_parser=StrOutputParser(),
                                 human_prompt_text=prompt_template,
                                 partial_variables={'content': user_personal_info + '\n' + user_theory_report})

    result = await simple_streamer.execute(chain=chain)

    return QuestionnaireRespType(id=analysis_input.session_id, content=result)


async def stream_multi_theory_report(analysis_input: MultiTheoryInputType):
    psycho_dict = psycho_theory_dict()
    if analysis_input.theory_id in psycho_dict:
        theory_obj: MultiTheoryDataType = psycho_dict[analysis_input.theory_id]
        simple_factory = SimplePromptFactory(llm_model=get_gpt_model(),
            trace_langfuse=True, trace_name='Multi_Theory_Report')
        simple_streamer = SimplePromptStreamer(socket_id=analysis_input.user_id, session_id=analysis_input.session_id,
                                               event_tag=SocketEvent.bot)

        dimension_concat = '\n'.join(theory_obj.dimension)

        chain = simple_factory.create_chain(output_parser=StrOutputParser(),
                                            human_prompt_text=MULTI_THEORY_CREATION_PROMPT,
                                            partial_variables={'theory': theory_obj.name,
                                                               'dimension': dimension_concat,
                                                               'personal_info': analysis_input.content})

        result = await simple_streamer.execute(chain=chain)

        return result

    return ''

async def stream_mix_theory_report(analysis_input: MixTheoryInputType):
    psycho_dict = psycho_theory_dict()
    theory_dimension_list: list[str] = []
    theory_name_list: list[str] = []

    # selected_questionnaire_list: list[MultiTheoryDataType] = []
    # for index, theory in enumerate(GLOBAL_PSYCHO_THEORY_ARRAY.theory):
    #     if theory.id in analysis_input.theory_id:
    #         selected_questionnaire_list.append(theory)

    for p_theory in analysis_input.theory_id:
        if p_theory in psycho_dict:
            theory = psycho_dict[p_theory]

            theory_name_list.append(theory.name)
            theory_dimension_list.append('. '.join(theory.dimension) + '\n')

    simple_streamer = SimplePromptStreamer(socket_id=analysis_input.user_id, session_id=analysis_input.session_id,
                                           event_tag=SocketEvent.bot)
    simple_factory = SimplePromptFactory(llm_model=get_gemini_model(Gemini_Model_1_5),
        trace_langfuse=True, trace_name='Multi_Theory_Report')
    chain = simple_factory.create_chain(output_parser=StrOutputParser(),
                                        human_prompt_text=MIX_THEORY_CREATION_PROMPT,
                                        partial_variables={'theory': ','.join(theory_name_list),
                                                           'dimension': ';'.join(theory_dimension_list),
                                                           'personal_info': analysis_input.content})

    result = await simple_streamer.execute(chain=chain)

    return result

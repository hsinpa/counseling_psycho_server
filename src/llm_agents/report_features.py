import uuid

from langchain_core.output_parsers import StrOutputParser

from src.llm_agents.llm_model import get_model, LLMModel
from src.model.questionnaire_model import QuestionnaireRespType
from src.types.router_input_type import InputMediaStrategyType, AnalysisInputQuestionnairesType
from src.utility.simple_prompt_factory import SimplePromptFactory
from src.utility.simple_prompt_streamer import SimplePromptStreamer
from src.utility.static_text import Gemini_Model_1_5, OpenAI_Model_3_5
from src.utility.utility_method import group_user_persoanl_info, group_user_input_theory_quiz


async def output_individual_strategy(user_input: InputMediaStrategyType, prompt_template: str):
    simple_streamer = SimplePromptStreamer(user_id=user_input.user_id, session_id=user_input.session_id)

    factory = SimplePromptFactory(model_name=OpenAI_Model_3_5, llm_model=LLMModel.OpenAI)

    chain = factory.create_chain(output_parser=StrOutputParser(),
                                 human_prompt_text=prompt_template,
                                 partial_variables={'content': user_input.content})

    result = await simple_streamer.execute(chain=chain)

    return QuestionnaireRespType(id=user_input.session_id, content=result)


async def output_theory_report(analysis_input: AnalysisInputQuestionnairesType, prompt_template: str):
    user_personal_info = group_user_persoanl_info(analysis_input.user_meta)
    user_theory_report = group_user_input_theory_quiz(analysis_input.question_answer_pairs)

    simple_streamer = SimplePromptStreamer(user_id=analysis_input.user_id, session_id=analysis_input.session_id)
    factory = SimplePromptFactory(model_name=OpenAI_Model_3_5, llm_model=LLMModel.OpenAI)

    chain = factory.create_chain(output_parser=StrOutputParser(),
                                 human_prompt_text=prompt_template,
                                 partial_variables={'content': user_personal_info + '\n' + user_theory_report})

    result = await simple_streamer.execute(chain=chain)

    return QuestionnaireRespType(id=analysis_input.session_id, content=result)

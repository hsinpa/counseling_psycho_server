import uuid

from langchain_core.output_parsers import StrOutputParser

from src.model.questionnaire_model import QuestionnaireRespType
from src.types.router_input_type import InputMediaStrategyType, AnalysisInputQuestionnairesType
from src.utility.simple_prompt_factory import SimplePromptFactory
from src.utility.utility_method import group_user_persoanl_info, group_user_input_theory_quiz


async def output_individual_strategy(user_input: InputMediaStrategyType, prompt_template: str):
    factory = SimplePromptFactory()

    chain = factory.create_chain(output_parser=StrOutputParser(),
                                 human_prompt_text=prompt_template,
                                 partial_variables={'content': user_input.content})
    result = await chain.ainvoke({})

    return QuestionnaireRespType(id=str(uuid.uuid4()), content=result)


async def output_theory_report(analysis_input: AnalysisInputQuestionnairesType, prompt_template: str):
    user_personal_info = group_user_persoanl_info(analysis_input.user_meta)
    user_theory_report = group_user_input_theory_quiz(analysis_input.question_answer_pairs)

    factory = SimplePromptFactory()

    chain = factory.create_chain(output_parser=StrOutputParser(),
                         human_prompt_text=prompt_template,
                         partial_variables={'content': user_personal_info + '\n' + user_theory_report})

    results = ''
    async for chunk in chain.astream({}):
        results = results + chunk

    return QuestionnaireRespType(id=str(uuid.uuid4()), content=results)

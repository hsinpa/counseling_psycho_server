import json

from langchain_core.output_parsers import StrOutputParser

from src.feature.llm_model import get_gemini_model
from src.feature.talk_simulation.detail_report.report_theory_prompt import PICK_THEORY_SYSTEM_PROMPT, \
    PICK_THEORY_HUMAN_PROMPT
from src.model.multi_theory_model import MultiTheoryDataType
from src.utility.simple_prompt_factory import SimplePromptFactory
from src.utility.theory_utility import GLOBAL_PSYCHO_THEORY_TEXT, GLOBAL_PSYCHO_THEORY_ARRAY
from src.utility.utility_method import parse_block


async def select_theory_chain(basic_info: str, questionnaire_full_text: str):
    response_schema = {
        "type": "object",
        "properties": {
            "theories": {
                "type": "array",
                "items": {
                    "type": "integer",
                }
            }
        }
    }

    prompt_factory = SimplePromptFactory(llm_model=get_gemini_model(json_schema=response_schema))
    chain = prompt_factory.create_chain(
        output_parser=StrOutputParser(),
        system_prompt_text=PICK_THEORY_SYSTEM_PROMPT,
        human_prompt_text=PICK_THEORY_HUMAN_PROMPT,
        partial_variables={
            'basic_info': basic_info,
            'theories': GLOBAL_PSYCHO_THEORY_TEXT,
            'questionnaire': questionnaire_full_text
        }
    ).with_config({"run_name": 'Pick Report Theory'})

    r = await chain.ainvoke({})

    q_json = json.loads(parse_block('json', r))

    selected_questionnaire_list: list[MultiTheoryDataType] = list(map(lambda x: GLOBAL_PSYCHO_THEORY_ARRAY.theory[x], q_json['theories']))

    return selected_questionnaire_list

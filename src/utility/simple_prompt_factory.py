from langchain_core.output_parsers import BaseOutputParser
from langchain.schema.messages import SystemMessage
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_openai.chat_models.base import BaseChatOpenAI
from langfuse.callback import CallbackHandler

from src.llm_agents.llm_model import LLMModel, get_model
from src.utility.static_text import OpenAI_Model_3_5

load_dotenv()

class SimplePromptFactory():
    """A factory only accept and run one prompt, nothing more"""

    def __init__(
            self,
            temperature: float = 0.75,
            llm_model: LLMModel = LLMModel.OpenAI,
            model_name: str = OpenAI_Model_3_5,
            json_response: bool = False,
            trace_langfuse: bool = True,
            trace_name: str = None
    ):
        kwargs = {'model_name': model_name, 'model': model_name, 'temperature': temperature}
        if json_response is True:
            kwargs['response_format'] = {"type": "json_object"}

        if trace_langfuse is True:
            self._langfuse_handler = CallbackHandler(user_id='hsinpa')

        self._llm: BaseChatOpenAI = get_model(model_enum=llm_model, **kwargs)
        self.trace_name = trace_name

    def create_chain(
            self,
            output_parser: BaseOutputParser,
            human_prompt_text: str,
            system_prompt_text: str = None,
            input_variables: list[str] = None,
            partial_variables: dict = None,
    ):

        if partial_variables is None:
            partial_variables = {}
        if input_variables is None:
            input_variables = []
        if system_prompt_text is None:
            system_prompt_text = "You are a helpful assistant."

        prompt = self._create_prompt(system_prompt_text, human_prompt_text, input_variables, partial_variables)
        chain = prompt | self._llm | output_parser
        chain = chain.with_fallbacks([chain])

        if self._langfuse_handler is not None:
            chain = chain.with_config({"callbacks": [self._langfuse_handler]})

        if self.trace_name is not None:
            chain = chain.with_config({"run_name": self.trace_name})

        return chain

    def _create_prompt(self, system_prompt:str, human_prompt: str, input_variables: list[str], partial_variables: dict ):
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessagePromptTemplate.from_template(human_prompt),
        ]

        template = ChatPromptTemplate(
            messages=messages, input_variables=input_variables, partial_variables=partial_variables
        )

        return template


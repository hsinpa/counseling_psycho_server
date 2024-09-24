from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import BaseOutputParser
from langchain.schema.messages import SystemMessage
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.prompts import AIMessagePromptTemplate
from langfuse.callback import CallbackHandler

from src.utility.simple_factory_type import simple_message_convert, messages_langchain_convert


class SimplePromptFactory:
    """A factory only accept and run one prompt, nothing more"""

    def __init__(
            self,
            llm_model: BaseChatModel,
            trace_langfuse: bool = False,
            trace_name: str = None
    ):
        self._langfuse_handler = None

        if trace_langfuse is True:
            self._langfuse_handler = CallbackHandler(user_id='hsinpa')

        self._llm = llm_model
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

    def _create_prompt(self, system_prompt: str, message_prompt: str, input_variables: list[str],
                       partial_variables: dict):
        # messages = [
        #     SystemMessage(content=system_prompt),
        #     HumanMessagePromptTemplate.from_template(message_prompt),
        # ]

        messages = messages_langchain_convert(
            simple_message_convert(system_prompt, message_prompt)
        )
        #
        # print(messages)
        template = ChatPromptTemplate(
            messages=messages,
            input_variables=input_variables,
            partial_variables=partial_variables
        )

        return template

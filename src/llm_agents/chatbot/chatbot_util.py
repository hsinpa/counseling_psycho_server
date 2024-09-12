from src.llm_agents.chatbot.chatbot_agent_type import TripleType


def convert_triple_str_to_pydantic(triple_str: str) -> TripleType | None:
    try:
        s_triple = triple_str.split("|")
        triple = TripleType(
            host_node= s_triple[0].strip(),
            relation=s_triple[1].strip(),
            child_node=s_triple[2].strip()
        )
        return triple
    except Exception as e:
        print(f'convert_triple_str_to_pydantic error {triple_str}, {e}')
    return None


def convert_triple_list_to_pydantic(triple_list: list[str]) -> list[TripleType]:
    triple_converts: list[TripleType] = []
    for t in triple_list:
        convert_t = convert_triple_str_to_pydantic(t)
        if convert_t is not None:
            triple_converts.append(convert_t)

    return triple_converts

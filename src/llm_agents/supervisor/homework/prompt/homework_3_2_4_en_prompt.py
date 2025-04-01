HOMEWORK_3_2_4_ASSIGNMENT_PROMPT = """\
You are a psychologist. Based on the conversation records, action plan, and Knowledge Graph, create a suitable homework assignment for this therapy session.

given conversation:
{conversation}

given action_plan:
{action_plan}

given knowledge_graph:
{knowledge_graph_issue}

output format:
{{Homework Title N: "",
Goal: "",
Task: "",
Step: ,
Example:
}},
{{Reflection Questions (for next session): ,
Question n: ""
}}\
"""
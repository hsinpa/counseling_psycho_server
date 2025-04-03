HOMEWORK_3_2_4_ASSIGNMENT_PROMPT = """\
You are a psychologist. Based on the conversation records, action plan, and Knowledge Graph, create a suitable homework assignment for this therapy session.

given conversation:
{conversation}

given action_plan:
{action_plan}

given knowledge_graph:
{knowledge_graph_issue}


Last output in JSON format, with following format

```json
{{
    "homeworks": [
        {{
            "title": "title of homework",
            "goal": "Goal of homework",
            "task": "The action to take for homework", 
            "steps": [
                How to accomplish this homework in steps
            ]
        }}
    ],
    "reflection_questions": [
        The possible reflection questions for next session, in string format
    ]
}}
```
"""
HOMEWORK_3_2_4_ASSIGNMENT_PROMPT = """\
You are a psychologist. Based on the conversation records, action plan, and Knowledge Graph, create a suitable homework assignment for this therapy session.

given conversation:
```
{conversation}
```
given action_plan:
```
{action_plan}
```
given knowledge_graph:
```
{knowledge_graph_issue}
```

output requirements:
Based on the information from the Knowledge Graph of the issue, extract relevant insights from the conversation to design a series of homework assignments.
1. Design 1-3 homework assignments based on this session's dialogue. The homework must include both cognitive and behavioral components.
2. To encourage clients to self-reflect between sessions, create three questions based on this week’s assignment, each consisting of only one question. The goals are to increase self-awareness, enhance cognitive restructuring, develop emotion regulation skills, and promote behavioral activation, laying the foundation for the next phase of treatment.

Last output in JSON format, with following format

```json
{{
    "homeworks": [
        {{
            "title": "title of homework",
            "goal": "Goal of homework",
            "task": "The action to take for homework", 
            "steps": [
                {{
                    "plan": "string type; Executable plan step on this homework; in string format",
                    "example": "string type; one concrete example on how patient can perform the plan step in daily life"
                }}
            ]
        }}
    ],
    "reflection_questions": ["The possible reflection questions for next session"]
}}
```
"""
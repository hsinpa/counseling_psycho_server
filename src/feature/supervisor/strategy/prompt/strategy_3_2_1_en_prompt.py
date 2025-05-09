STRATEGY_PROMPT_3_2_1_NEXT_THERAPY_GOAL = """\
You are a psychologist. Based on the treatment issues and objectives, treatment effectiveness, Knowledge Graph, and the Next Session Therapy Direction, provide the next therapy goal for each treatment issue.

given treatment_issue_and_objective:
{therapy_issue_and_objective}

given treatment_effectiveness:
{treatment_effectiveness}

given knowledge_graph:
{knowledge_graph_issue}

given next_session_therapy_direction:
{next_session_therapy_direction}

Output Requirement: Design the next therapy goal for each treatment issue, from Issue 1 to Issue N, by sequence.

Output JSON, with the format as follow

```json
{{
    "next_therapy_goals": [
        {{
            "issue": "The name of issue",
            "goal": "",
        }}
    ]
}}
```\
"""
PREREQUISITE_PROMPT_3_1_THERAPY_DIRECTION = """\
You are a psychologist. Based on the following therapy progress and therapy_effectiveness, outline the next steps in therapy.

given progress:
{progress}

given treatment_effectiveness:
{treatment_effectiveness}

Output Requirements:

Include both long-term and next-session therapy directions:
Long-term Therapy Direction, Short-to-Mid-term Therapy Direction, Next Session Therapy Direction

Output in JSON format, the schema is define as follows
```json
{{
    "long_term_therapy_direction": "",
    "short_to_mid_term_therapy_direction": "",
    "next_session_therapy_direction": "",
}}
```\
"""
CASE_TREATMENT_PROMPT_3_2_1_STRATEGY = """
You are a psychologist. Based on the given case treatment information, methods, and therapeutic hierarchy, develop a step-by-step treatment strategy for each issue.

given Case_Treatment_Information:
{case_treatment_information}

given Methods:
{method}

therapeutic_hierarchy:
{therapeutic_hierarchy}

Output Requirements: Must include three main components:
(1) Number of steps
(2) Goals for each stage
(3) Implementation methods. Analyze each issue individually. When designing the steps, prioritize the client's emotional stability and stress reduction.
Also, consider where the issue appears within the overall treatment framework, and use that to develop a customized step-by-step intervention plan.

Note: Before scheduling any behavioral activity, ensure there is a preceding step focused on emotional stabilization.
Choosing the focus of the column 'steps' with special care: to prioritize treatment focus, it is necessary to include the cognitive, emotional, and behavioral dimensions. (e.g. cognition - emotion - behavior)

Output in JSON format, the schema is define as follows
```json
{{
    "issues": [
    {{
        "issue": "name of the issue",
        "focus_of_stepped_care": "to prioritize treatment focus, it is necessary to include the cognitive, emotional, and behavioral dimensions. (e.g. cognition - emotion - behavior)",
        "goal": "goal of issue",
        "steps": [
            {{
                "title": "title of this step",
                "therapeutic_goal": "",
                "explanation_of_technique": ""
            }}
        ]
    }}
    ]
}}
```\
"""
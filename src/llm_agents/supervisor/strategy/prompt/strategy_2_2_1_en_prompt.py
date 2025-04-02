STRATEGY_PROMPT_2_2_1_MEAN_OF_AT = """\
You are a psychologist. Given the core belief and intermediate belief and cognitive models, infer the meaning of automatic thought in each situation based on the client's core belief.

given core_belief_and_intermediate_belief:
{core_belief_and_intermediate_belief}

given cognitive_model:
{cognitive_model}

Note: mean of A.T. refers to one of the core beliefs.\

Lastly output in JSON format as following:
```json
{{
    "situations": [
        {{
            "situation": "",
            "mean_of_AT": ""
        }}
    ]
}}
```
"""
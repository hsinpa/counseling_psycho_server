STRATEGY_PROMPT_2_1_COGNITIVE_MODEL = """\
You are a psychologist. Based on the conversation record, identify and mark the client's cognitive model for each situation.

given conversation:
{conversation}

given situation:
{client_situations}

Output Requirements: Label each situation.
Automatic Thought\\ refers to a spontaneous and often subconscious thought that arises in the client when facing a particular situation, and it influences their emotional and behavioral responses.
Emotion\\ A subjective feeling triggered by a situation or thought, which affects physiological and behavioral responses.
Physiological Response\\ The body's automatic reaction to emotions, such as changes in heart rate, muscle tension, or energy levels.
Behavior\\ Observable external behaviors (e.g., social withdrawal), excluding internal mental processes (e.g., suicidal ideation, rumination).

Lastly output in JSON format as following:

```json
{{
    "cognitive_model": [
        {{
            "situation": "",
            "automatic_thought": "",
            "emotion": "",
            "physiological_response": "",
            "behavior": ""
        }}
    ]
}}
```
"""
STRATEGY_PROMPT_2_1_COGNITIVE_MODEL = """\
You are a psychologist. Based on the conversation record, identify and mark the client's cognitive model for each situation.

given conversation:
{conversation}

Output Requirements: Summarize events that evoke the client's feelings into major categories as "situations" and present them in bullet points.
Situation\\  refers to an external event, internal experience, or physical state that triggers a cognitive or emotional response. It can include environmental occurrences, social interactions, physiological sensations, or personal experiences that initiate a thought process.
Automatic Thought\\ A spontaneous and often subconscious thought that arises in response to a situation, influencing emotions and behavior.
Emotion\\ A subjective feeling triggered by a situation or thought, which affects physiological and behavioral responses.
Physiological Response\\ The body's automatic reaction to emotions, such as changes in heart rate, muscle tension, or energy levels.
Behavior\\ The actions taken in response to a situation, thought, or emotion, which can reinforce or alter future experiences.

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
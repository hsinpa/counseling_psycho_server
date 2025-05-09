STRATEGY_PROMPT_2_1_1_SITUATIONS = """\
You are a therapist. Based on the conversation record,identify and label the type of each situation the client is experiencing, and provide a clear description.

Situation Type:
Type 1: The client has not taken any concrete action. When describing the situation, start with the time, followed by the event and the client’s thoughts.
Type 2: The client has engaged in actual behavior. When describing the situation, start with the time, followed by the event (excluding thoughts).

given conversation:
{conversation}

output requirement: The marked situation must be an event that triggers negative thoughts in the client. 
A complete situation is not a single moment, but a psychologically meaningful unit of experience that unfolds around the same event.

output format:
{{Situation Type: ,
Action: Y/N,
Negative Thought: Y,
Time: The time during which an experience takes place(e.g., in the morning, during work, on a holiday),
Environmental setting: (e.g., alone in a room, during a meeting, after a breakup)
Client’s subjective thoughts: (e.g., feeling exhausted, seeing a message, remembering something painful),
Situation 1: Describe, in one sentence, the event that triggered the client's negative thinking.
{{Situation Type: ,
Action: Y/N,
Negative Thought: Y,
Time: ,
Environmental setting: "",
Client’s subjective thoughts: "",
Situation N:
}}\
"""
STRATEGY_PROMPT_2_2_CORE_INTERMEDIATE_BELIEF = """\
You are a psychologist. Label the following conversation record with several Cognitive Models. Based on the conversation record and Cognitive Models, infer the client's core beliefs and intermediate beliefs.

given conversation:
{conversation}

given cognitive_model:
{cognitive_model}

Core Belief Type
Helpless Core Beliefs
"I am incompetent."
"I am ineffective."
"I can't do anything right."
"I am helpless."
"I am powerless."
"I am weak."
"I am vulnerable."
"I am a victim."
"I am needy."
"I am trapped."
"I am out of control."
"I am a failure."
"I am defective" [i.e., I do not measure up to others].
"I am not good enough" [in terms of achievement].
"I am a loser."
Unlovable Core Beliefs
"I am unlovable."
"I am unlikeable."
"I am undesirable."
"I am unattractive."
"I am unwanted."
"I am uncared for."
"I am different."
"I am bad" [so others will not love me].
"I am defective" [so others will not love me].
"I am not good enough" [to be loved by others].
"I am bound to be rejected."
"I am bound to be abandoned."
"I am bound to be alone."
Worthless Core Beliefs
"I am worthless."
"I am unacceptable."
"I am bad."
"I am a waste."
"I am immoral."
"I am dangerous."
"I am toxic."
"I am evil."
"I don't deserve to live."

Output Requirements:
Summarize situations 1 to n into a single Core Belief and organize Intermediate Beliefs (attitudes and assumptions).

Output format:
{{
[Core Belief Type: Helplessness, Unlovability, or Worthlessness,
Explanation: Based on the above core belief categories, analyze the conversation record and summarize the client's core beliefs,
Client's Core Belief: Find suitable sentences from the core belief types for summarization, list them in order, and number them.
],
[Intermediate Belief n: "",
Positive Assumption: "",
Negative Assumption: "",
]
}}
note: Intermediate beliefs are the client's attitudes and assumptions about themselves and the world.\
"""
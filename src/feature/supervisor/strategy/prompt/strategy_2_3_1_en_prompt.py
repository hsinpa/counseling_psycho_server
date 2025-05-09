STRATEGY_PROMPT_2_2_1_RELEVANT_HISTORY_PRECIPITANTS = """\
You are a psychologist. Based on the Cognitive Model, conversation, Core Belief, and Intermediate Belief, identify and mark the client's relevant life history and precipitants. List key points.

given conversation:
{conversation}

given cognitive_model:
{cognitive_model}

given core_belief_and_intermediate_belief:
{core_belief_and_intermediate_belief}

Output Requirements:
Based on the cognitive model and conversation, compile a bullet point summary of relevant life history and the precipitants that trigger core beliefs.
Relevant life history includes significant events such as ongoing or periodic family conflict, parental divorce, and negative interactions with parents, siblings, teachers, or peers in which the child felt blamed, criticized, or devalued. Other factors may include serious medical conditions or disabilities, the loss of significant others, bullying, physical or sexual abuse, emotional trauma, and adverse life circumstances such as frequent relocations, poverty, trauma, or chronic discrimination. Additionally, youths may have perceived—whether accurately or not—that they did not measure up to their siblings, were different from or demeaned by peers, failed to meet the expectations of parents, teachers, or others, or that their parents favored a sibling over them.

Output in JSON format as follows:
```json
{{
    "relevant_life_history": [key point],
    "precipitants": [precipitants to the current disorder]
}}
```
"""
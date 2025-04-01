STRATEGY_PROMPT_2_3_4_KNOWLEDGE_GRAPH_ISSUE = """\
You are a psychologist. Based on the given therapy issue, cognitive model, core belief and intermediate belief, coping strategy, relevant history, and precipitants, create a Knowledge Graph for each issue. Present the relationships in a triple format:
Triple format: ( head, relation, tail )

given therapy_issue_and_objective:
{therapy_issue_and_objective}

given cognitive_model:
{cognitive_model}

given core_belief_and_intermediate_belief:
{core_belief_and_intermediate_belief}

given coping_strategy:
{coping_strategy}

given relevant_history_and_precipitants:
{relevant_history_and_precipitants}

given situations_relevant_to_issue:
{situations_relevant_to_issue}

Relationships between nodes in the Knowledge Graph:
(Relevant History, Shapes, Core Beliefs)
(Relevant History, Influences, Precipitant)
(Precipitant, Triggers, Core Beliefs)
(Precipitant, Facilitates, Situation)
(Issue, Shapes, Situation)
(Situation, Facilitates, Automatic Thoughts)
(Automatic Thoughts, Generate, Emotions)
(Automatic Thoughts, Generate, Behavior)
(Automatic Thoughts, Are Affected By, Core Beliefs)
(Core Beliefs, Generate, Automatic Thoughts)
(Automatic Thoughts, Lead To, Coping Strategies)
(Coping Strategies, Generate, Behavior)
(Core Beliefs, Generate, Intermediate Beliefs)
(Intermediate Beliefs, Generate, Coping Strategies)

Output Requirement:
Step by step, create a Knowledge Graph for each issue with relevant connections:
Use the issue as the main axis and identify related situations.
Compare the issue and situations, then extract the relevant history and core beliefs associated with the issue, removing any unrelated parts.
Compare the issue and situations, and list the emotions, behaviors, and automatic thoughts related to the situations.
Compare the issue and situations, remove unrelated elements, and select the intermediate beliefs relevant to the situations. Then, list the coping strategies associated with these intermediate beliefs.

Output Format:
{{Knowledge Graph 1:

}},
{{Knowledge Graph N:

}}

Note: List the content of each head and tail in the Knowledge Graph.\
"""
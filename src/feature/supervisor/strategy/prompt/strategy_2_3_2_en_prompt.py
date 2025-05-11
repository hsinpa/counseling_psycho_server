STRATEGY_PROMPT_2_3_2_COPING_STRATEGY= """\
You are a psychologist. Based on the Cognitive Model, conversation, Core Belief, Intermediate Belief, Relevant Life History, and Precipitants, 
derive the client's coping strategy under this Intermediate Belief. 
List key points.

given conversation:
{conversation}

given cognitive_model:
{cognitive_model}

given core_belief_and_intermediate_belief:
{core_belief_and_intermediate_belief}

given relevant_history_and_precipitants:
{relevant_history_and_precipitants}

Example of Intermediate Belief:
Therapist: What’s your belief about asking for help? [Avoiding asking
for help is a coping strategy.]
Client: Oh, asking for help is a sign of weakness, incompetence.
Therapist: What’s the worst that could happen if you don’t try to look
your best? [“I should always look my best” is the client’s rule.]
Client: People will think I’m unattractive; they won’t want me
around.
Therapist: What would it mean to you if you didn’t achieve highly? [“I
have to achieve highly” is the rule; “It’s terrible to be mediocre” is
the client’s attitude.]
Client: It shows I’m inferior to other people.
Therapist: What’s bad about experiencing negative emotion? [“I
shouldn’t let myself get upset” is the rule; “It’s bad to experience
negative emotion” is the attitude.]
Client: If I do, I’ll lose control.
Therapist: What are the advantages of not sticking out in a crowd?
[Avoiding sticking out in a crowd is a coping strategy.]
Client: People won’t notice me. They won’t see that I don’t fit in.
Therapist: How would you fill in this blank? If I even try to make
plans with other people, then ? [Avoiding making
plans is a coping strategy.]
Client: They’ll turn me down because I have nothing to offer them.

Output Requirements:
Based on the above information, analyze the client's rules, attitudes, and coping strategies under the Intermediate Beliefs.
Coping Strategy: The client's coping measures based on these assumptions.

Output in json format as follow:
{{
    "strategies": [
        title: "The concise and short name of this strategy. Maximum two words, and can not be duplicate to other strategies",
        "summary": "string type, maladaptive coping strategies related to the Core Belief and Intermediate Belief",
        "rule": "string type,the client's understanding of things based on these assumptions",
        "attitude": "string type, the client's attitude toward things under these assumptions"
    ]
}}
"""
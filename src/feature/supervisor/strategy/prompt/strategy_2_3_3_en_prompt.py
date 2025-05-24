STRATEGY_PROMPT_2_3_3_SITUATION_RELEVANT_ISSUE = """\
You are a psychologist. Based on the therapy issue and objective, as well as the Cognitive Model, identify situations relevant to the issue.

given therapy_issue_and_objective:
{therapy_issue_and_objective}

given cognitive_model:
{cognitive_model}

output requirement:
From Issue 1 to Issue N, mark each situation related to the issue accordingly, ensuring that every issue and situation is accounted for and properly labeled.

Output Format:

{{Issue N: situations number relevant to the issue
}}\
"""
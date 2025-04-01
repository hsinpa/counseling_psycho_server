PREREQUISITE_PROMPT_1_5_THERAPY_OUTCOME = """\
You are a psychologist. Based on the conversation record, therapy issues, objectives, and annotated treatment methods and techniques, analyze the therapeutic outcomes of this session and mark the client's emotional state transitions.

given conversation:
{conversation}

given therapy_issue_and_objective:
{therapy_issue_and_objective}

given methods_and_techniques:
{methods_and_techniques}

Output Requirements:
For each therapy issue, compare the therapy objective with the applied methods and techniques, analyze the therapeutic outcome, and mark the client’s emotional state transition.

{{Therapy Issue: List the therapy issue (Tn-Tn)
[Therapeutic Outcome: Based on the therapy objective, compare with the applied methods and techniques, and describe the client's state after treatment,
Client's Emotional Transition: List the client's emotional state before the therapist's intervention and after receiving the therapist’s response, marked in a triple format],
}}

triple:(Client’s initial emotional state, more optimistic or pessimistic, Client’s transitioned emotional state)\
"""
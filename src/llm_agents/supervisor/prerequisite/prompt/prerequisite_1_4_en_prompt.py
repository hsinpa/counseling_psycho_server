PREREQUISITE_PROMPT_1_4_TREATMENT_PROGRESS = """\
You are a psychologist. Based on the conversation record, treatment framework annotations, and therapy issues and objectives, determine whether each issue falls into the early, middle, or late stage of the therapeutic process. Additionally, based on the therapeutic objectives and assigned homework, determine whether this conversation record represents the early, middle, or late stage of the overall treatment process and provide an explanation.

given conversation:
{conversation}

given treatment_framework:
{treatment_framework}

given therapy_issue_and_objective:
{therapy_issue_and_objective}

Output Requirements:
The output should be divided into two parts:
1. Classification of N therapy issues into early, middle, or late stage of treatment.
2. Assessment of whether this conversation record represents an early, middle, or late stage of the treatment process, based on the assigned homework and the therapeutic objectives.

{{Therapy Issues: "Tn-Pn: Description of the issue"
[Treatment Process: Determine whether this issue falls into the early, middle, or late stage of treatment for the client based on the degree of resolution,
Explanation: Explanation of the treatment process and rationale for classification
]}}

{{Treatment Progress: This conversation record represents which stage of the treatment process
[Homework: List the assigned homework,
Explanation of Treatment Progress: Justification for determining the stage,
Next Stage Treatment Recommendations: Provide suggestions for the next phase of treatment
]}}\
"""
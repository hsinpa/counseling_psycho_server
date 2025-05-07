PREREQUISITE_PROMPT_1_6_TREATMENT_EFFECTIVENESS = """\
You are a psychologist. Based on the treatment progress and therapeutic outcomes, assess the effectiveness of the treatment and provide an explanation.

given progress:
{progress}

given therapy_outcome:
{therapy_outcome}

Output Requirements:
The output should be divided into two parts: Treatment Effectiveness Summary and Treatment Effectiveness Indicators.

{{Treatment Effectiveness Summary:
[Cognitive Aspect: "",
Behavioral Aspect: "",
Emotional Aspect: "",
Self-Worth Aspect: ""
]}}

{{Treatment Effectiveness Indicators: (Therapy Issue, Client’s initial emotional state, Current State, Treatment Effectiveness and Explanation)
}}\
"""
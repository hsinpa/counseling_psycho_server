PREREQUISITE_PROMPT_1_1_TREATMENT_FRAMEWORK = """\
You are a psychologist. Based on the Cognitive Behavioral Therapy (CBT) framework, annotate the following conversation record by marking the therapeutic structure and specifying the techniques used within the framework.

Therapeutic Structure Strategies for the First Session:
Initial Part of Session 1
1. Set the agenda (and provide a rationale for doing so).
2. Conduct a mood check.
3. Obtain an update (since the evaluation).
4. Discuss the patient's diagnosis and provide psycho education.

Middle Part of Session 1
5. Identify problems and set goals.
6. Educate the patient about the cognitive model.
7. Discuss a specific problem.

End of Session 1
8. Provide or elicit a summary.
9. Review the homework assignment.
10. Elicit feedback.

Therapeutic Structure Strategies for Subsequent Sessions:
Initial Part of Session
1. Conduct a mood check.
2. Set the agenda.
3. Obtain an update.
4. Review homework.
5. Prioritize the agenda.

Middle Part of Session
6. Work on a specific problem and teach CBT skills within that context.
7. Follow up with relevant, collaboratively set homework assignments.
8. Work on a second problem.

End of Session
9. Provide or elicit a summary.
10. Review new homework assignments.
11. Elicit feedback.

given conversation:
{conversation}

Output Requirements:
The output must include both the therapeutic structure and the techniques used in each section. 
The therapeutic structure should be divided into three parts, marking the specific techniques applied within each section and explaining the criteria for differentiation.

Format the output as follows:
{{Initial Part of Session:
Set the agenda: Tn,
Mood check: Tn,
Obtain an update: Tn,
Discuss the patient's diagnosis and provide psycho education: Tn,
Review homework: Tn,
Prioritize the agenda: Tn
}}
{{Middle Part of Session:
Identify problems and set goals: Tn,
Educate the patient about the cognitive model: Tn,
Discuss a problem: Tn,
Work on a specific problem and teach CBT skills within that context: Tn,
Follow-up discussion with relevant, collaboratively set homework assignments: Tn,
Work on a second problem: Tn
}}
{{End of Session:
{{Provide or elicit a summary: Tn,
Review new homework assignments: Tn,
Elicit feedback: Tn
}}
"""
CASE_TREATMENT_PROMPT_3_2_0_INFORMATION = """
You are a psychotherapist. Given treatment framework, Knowledge Graph of issues,symptoms and intervention techniques, analyze the client's condition and determine the appropriate treatment method.

given therapy_issue_and_objective:
{therapy_issue_and_objective}

given treatment_framework:
{treatment_framework}

given Knowledge_Graph_of_Issue:
{knowledge_graph_of_issue}

given Symptoms:
{symptoms}

given Intervention_Techniques:
{intervention_techniques}

Output Specification: There are a total of N issues, to be analyzed sequentially from Issue 1 to Issue N. 
It is necessary to consider the client's understanding of the issue at each point in the treatment framework, and to adjust the goals and areas of focus accordingly in order to design a customized intervention strategy.

Output in JSON format, the schema is define as follows
```json
{{
    "issues": [
    {{
        "issue": "name of the issue",
        "treatment_framework": "choose one or more sessions(Initial Part of Session/ Middle Part of Session/ End of Session)",
        "goal": "",
        "symptom": "",
        "symptom_characteristics": "",
        "intervention_technique_type": "choose from the eight major types",
        "specific_therapy_method": "a specific approach within the eight major types",
        "therapy_direction": "a specific approach within the eight major types",
        "treatment_difficulty": "a specific approach within the eight major types",
        "treatment_limitation": "a specific approach within the eight major types"    
    }}
    ]
}}
```\
"""
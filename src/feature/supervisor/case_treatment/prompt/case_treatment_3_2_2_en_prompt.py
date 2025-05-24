CASE_TREATMENT_PROMPT_3_2_2_EVALUATION = """
You are a psychotherapist. Based on the given case treatment information and case treatment strategy, 
set specific criteria for each step according to Distress Tolerance and Functional Capacity, 
and indicate which step to swift to if the criteria are not met.

given Case_Treatment_Information:
{case_treatment_information}

given case_treatment_strategy:
{case_treatment_strategy}

I. Distress Tolerance
I_1. Emotional Stability: Can the client remain calm during intense emotional episodes without resorting to impulsive behaviors (e.g., self-harm, avoidance)?
I_2. Stress Endurance: Is the client able to apply learned emotional regulation or coping strategies under stressful conditions? (e.g., deep breathing, self-soothing, self-talk)
I_3. Cognitive Awareness: Can the client recognize the source of their emotional fluctuations? Are they able to reflect on their thoughts and reactions?
I_4. Behavioral Control: Is the client able to delay their responses? Do they refrain from acting destructively or withdrawing due to emotional pain?

II. Functional Capacity
II_1. Daily Living Function: Is the client able to manage basic self-care independently? (e.g., eating, bathing, maintaining routines)
II_2. Social Role Performance: Is the client able to fulfill basic responsibilities and maintain interpersonal interactions within family, school, or work settings?
II_3. Self-Care Ability: Does the client remember to take medication, plan activities, and seek social support when needed?
II_4. Therapy Engagement: Is the client consistently attending therapy sessions, coming prepared, and actively participating in discussions and assignments?

Decision Rules:
1. Treatment Goal not achieved: If the current phase treatment goal has not been met, reinforce core skills such as emotional regulation and safety planning.
2. Low Distress Tolerance: If the patient demonstrates low distress tolerance, return to earlier steps focused on teaching foundational emotional regulation or impulse control.
3. Decreased Functional Capacity: If the patient shows reduced ability to function, return to more basic stages that involve behavioral activation or establishing daily structure.
4. Cognitive Restructuring not yet internalized: If core beliefs have not been successfully challenged, revisit guided discovery or Socratic questioning techniques.
5. Emerging Risk or Crisis: If new risks or crises emerge, return to the initial step of risk assessment and safety intervention.
6. Weak Therapeutic Alliance: If the therapeutic alliance is weak, go back to early steps focused on building safety and therapeutic connection.
7. Presence of emotional disturbance: If emotional disturbance is present, return to the step related to emotional soothing or relaxation training.

Output in JSON format, the schema is define as follows
```json
{{
    "issues": [
    {{
        "issue": "name of the issue",
        "steps": [
            {{
                "index": number (index number of this step),
                "phase_specific_evaluation_criteria": "",
                "challenge": "Description of the difficulty encountered",
                "emotional_disturbance": boolean type (true or false),
                "recommended_step_to_swift_to": "string type, Which step index to fallback, when patient is not doing as plan (Make a decision based on the Decision Rules and provide an explanation)"
                "recommended_swift_step_index": number type (The step index to fallback, check recommended_step_to_swift_to),
            }}
        ]
    }}
    ]
}}
```\
"""
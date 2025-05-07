PREREQUISITE_PROMPT_1_3_METHOD_TECH = """\
You are a psychologist. Based on the following conversation record, identify and annotate the therapeutic methods and techniques used from Judith Beck's Cognitive Behavior Therapy book.

given conversation:
{conversation}

Therapeutic Methods and Techniques
Cognitive Restructuring Techniques:
Identifying Automatic Thought\\ Includes explanation, guided questioning, confirmation, and teaching the patient to recognize automatic thoughts.
Evaluating Automatic Thoughts\\ Identifying key thoughts and evaluating them through Socratic questioning. The therapist should assess the overall evaluation outcome and determine when alternative questioning or responses are needed. Patients should be taught how to evaluate their own automatic thoughts to manage related issues effectively in daily life.
Identifying Emotions\\ Differentiating emotions, labeling them, and assessing their intensity.
Identifying and Modifying Intermediate Beliefs\\ Using the “downward arrow” technique to examine automatic thoughts and identify common attitudes.
Identifying and Modifying Core Beliefs\\ Using the “downward arrow” technique to explore automatic thoughts and detect recurring themes.
Behavioral Activation\\ Structuring activity planning to improve emotional states.

Improvement Techniques:
Problem-Solving\\ Encouraging the patient’s critical thinking through dialogue, designing and implementing solutions, and evaluating their effectiveness.
Decision-Making\\ Designing systematic assessment methods to help patients evaluate the pros and cons of each decision and reach conclusions.
Relaxation Training\\ Including guided imagery, muscle relaxation techniques, and controlled breathing exercises.
Refocusing\\ Designing strategies to help patients refocus on their current tasks.
Measuring Emotions and Behaviors\\ Using scales to assess the intensity of emotions or behaviors.
Graded Task Assignment\\ Breaking down goals into smaller steps to facilitate achievement.
Exposure Therapy\\ Encouraging patients to engage in anxiety-inducing activities daily while equipping them with coping techniques to reduce anxiety.
Role-Playing\\ Using role-playing to explore automatic thoughts, develop adaptive responses, and modify intermediate or core beliefs.
Using the Pie Technique\\ Utilizing pie charts to visually represent the patient’s thoughts, helping them set goals or analyze root causes.
Self-Comparison and Credit List\\ Encouraging patients to compare themselves with their lowest state and record positive aspects of their daily life.

Output Requirements:
Based on the conversation record, identify the therapeutic methods and techniques applied.

{{Therapeutic Methods and Techniques:
[Tn-Pn: Therapeutic method or technique, specify whether it falls under cognitive restructuring techniques or improvement techniques,
Explanation: Describe how it was applied
],
[Tn-Pn: Therapeutic method or technique, specify whether it falls under cognitive restructuring techniques or improvement techniques,
Explanation: Describe how it was applied
],
[Tn-Pn: Therapeutic method or technique, specify whether it falls under cognitive restructuring techniques or improvement techniques,
Explanation: Describe how it was applied
]}}\
"""
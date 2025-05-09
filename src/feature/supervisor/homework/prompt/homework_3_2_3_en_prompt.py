HOMEWORK_3_2_3_ACTION_PLAN_PROMPT = """\
You are a psychologist. Based on the conversation records and therapy issues, each selected therapy issue has an action plan. Compare it with the action plan type, label each action plan, and provide an explanation.

given conversation:
{conversation}

give therapy_issue_and_objective:
{therapy_issue_and_objective}

Action Plan Type
Reading Therapy Notes: Clients review and summarize key points to reinforce learning and action plans.
Monitoring Automatic Thoughts: Encourage clients to notice and record their thoughts when their mood changes.
Evaluating and Responding to Automatic Thoughts: Help clients modify inaccurate or unhelpful thoughts to improve their action plans.
Conducting Behavioral Experiments: Test negative predictions through real-life experiences to change cognition and emotions.
Disengaging from Unhelpful Thought Processes: Teach mindfulness techniques to reduce self-criticism, rumination, or obsessive thinking.
Implementing Steps Toward Goals: Collaborate with clients to plan action steps and overcome obstacles.
Engaging in Mood-Boosting Activities: Encourage participation in activities that promote self-care, social interaction, or a sense of achievement.
Creating a Self-Credit List: Keep track of daily achievements to build confidence and improve self-perception.
Practicing Behavioral Skills: Learn and apply problem-solving skills such as emotional regulation or time management.
Engaging in Bibliotherapy: Reinforce therapy concepts through reading relevant books or materials.
Preparing for the Next Therapy Session: Clients reflect on key topics beforehand to enhance therapy efficiency.

output format:

{{Issue 1: "",

action plan type: "",

Explanation: ""
}},

{{Issue N: "",

action plan type: "",

Explanation: ""

}}
"""
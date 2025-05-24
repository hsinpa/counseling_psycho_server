PREREQUISITE_PROMPT_1_2_THERAPY_OBJECTIVE = """\
You are a therapist. Based on the provided conversation record and the types of issues, identify and label the issues(please also explain the reason) and objectives for this therapy session.

given conversation:
{conversation}

[Types of Issues]
```
1. Personal/Internal Issues
Emotional Distress: Anxiety, depression, anger, loneliness, panic, emotional overwhelm
Self-Identity: Self-worth, self-esteem, internal conflicts, identity confusion, values conflict
Stress Management: Academic stress, work stress, chronic stress, burnout, life pressures
Trauma: Grief, PTSD, childhood trauma, emotional neglect, abuse history

2. Interpersonal Relationship Issues
Family Relationships: Parent-child conflict, sibling rivalry, family of origin issuesRomantic Relationships: Intimacy issues, communication problems, breakup recoveryFriendship & Social Issues: Social anxiety, loneliness, bullying, making/keeping friends

3. Life Adjustment Issues
Career Exploration: Career planning, exploring interests, feeling lost
Academic Adjustment: Study motivation, exam stress, time management
Major Life Changes: Moving, school transfer, graduation, unemployment, retirement
Cultural Adaptation: Cross-cultural experiences, immigration, studying abroad

4. Love and Sexuality Issues
Romantic Relationships: Emotional attachment, separation anxiety, love-related distress
Sexuality: Gender identity, sexual orientation, sexual trauma, sex education
Sexual Health/Functioning: Sexual anxiety, mismatched libido, sexual dysfunction

5. Mental Health / Clinical Issues
Mood Disorders: Depression, bipolar disorder, dysthymia, seasonal affective disorder
Anxiety Disorders: Generalized anxiety, social anxiety, panic disorder, OCD, phobias
Trauma-Related Disorders: PTSD, acute stress disorder, complex trauma reactions
Psychotic Disorders: Schizophrenia, schizoaffective disorder, delusional disorder
Eating Disorders: Anorexia nervosa, bulimia nervosa, binge eating disorder
Personality Disorders: Borderline, narcissistic, avoidant, dependent personality patterns
Neurodevelopmental and Cognitive Disorders: ADHD, autism spectrum disorder, learning disabilities
Substance Use and Addiction: Alcohol/drug dependence, behavioral addictions (e.g., gambling, gaming)
Somatic and Psychophysiological Symptoms: Psychosomatic pain, health anxiety, sleep disturbance, chronic fatigue

6. Self-Growth and Exploration
Meaning of Life: Searching for life direction and purpose
Spirituality: Faith, existential concerns, spiritual confusion
Creativity and Potential Development: Artistic growth, writing, entrepreneurship, personal expression

7. Suicide Risk
Hopelessness and Helplessness: Persistent feelings of despair, perceived lack of solutions, emotional numbness
Self-Harm and Suicidal Thoughts: Intrusive suicidal ideation, self-injury behavior, passive death wish
Loss and Isolation: Grief, social withdrawal, disconnection from support systems
Burden and Worthlessness: Feeling like a burden to others, chronic guilt, self-devaluation
Crisis and Impulsivity: Sudden life stressors, emotional overwhelm, lack of coping mechanisms
```

Output Requirements:
The conversation consists of N statements. Identify and classify the client's issues based on the type of issue, and for each identified issue, label it and describe the therapeutic goal.
The size of therapeutic_issues, can not exceed seven issues

Note: Cognitive distortions should not be considered an issue.

[Rule of therapeutic_issue title]
```
A label from [Types of Issues]: title of this issue; Label the sentence intervals that are relevant to the therapeutic issue (e.g., T1–T10)

Give you a concrete example, what the title format should look like

Suicide Risk: Hopelessness and Helplessness (P-7, P-10, P-17, P-79, P-90)
```

therapeutic_issues
Output JSON, with the format as follow:
```json
{{
    "therapeutic_issues": [
        {{
            "title": "Check out [Rule of therapeutic_issue title]",
            "objective": "Explain the reason for addressing this issue and the expected outcome"
        }}
    ]
}}
```\
"""
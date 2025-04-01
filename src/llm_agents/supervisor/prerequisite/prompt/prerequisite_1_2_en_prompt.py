PREREQUISITE_PROMPT_1_2_THERAPY_OBJECTIVE = """\
You are a therapist. Based on the provided conversation record and the types of issues, identify and label the issues(please also explain the reason） and objectives for this therapy session.

given conversation:
{conversation}

Types of Issues
1. Personal/Internal Issues
Emotional Distress: Anxiety, depression, anger, loneliness, panic, etc.
Self-Identity: Self-worth, self-esteem, internal conflicts, identity crisis
Stress Management: Academic stress, work stress, life pressures
Trauma: Grief, PTSD, childhood trauma

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

5. Mental Health/Clinical Issues
Mood Disorders: Depression, bipolar disorder, anxiety disorders
Personality Disorders: Borderline, antisocial, narcissistic personality traits
Eating Disorders: Anorexia, bulimia, binge eating
Addiction Issues: Internet, alcohol, drugs, gambling addictions

6. Self-Growth and Exploration
Meaning of Life: Searching for life direction and purpose
Spirituality: Faith, existential concerns, spiritual confusion
Creativity and Potential Development: Artistic growth, writing, entrepreneurship, personal expression

7.Suicide Risk

Output Requirements:
The conversation consists of N statements. For each therapeutic issue, provide an annotation and describe the therapeutic objective.

Output format:
{{Therapeutic Issues:
[Tn-Tn: List the therapeutic issue,
Therapeutic Objective: Explain the reason for addressing this issue and the expected outcome
],
[Tn-Tn: List the therapeutic issue,
Therapeutic Objective: Explain the reason for addressing this issue and the expected outcome
],
[Tn-Tn: List the therapeutic issue,
Therapeutic Objective: Explain the reason for addressing this issue and the expected outcome
]}}\
"""
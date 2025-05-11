from io import BytesIO
from typing import List

from docx import Document

from src.feature.supervisor.supervisor_model import SupervisorAnalysisRespModel, CaseConceptualizationModel, \
    IssueTreatmentStrategy, HomeworkAssignment


class SupervisorDocxExporter:

# region Case Conceptualization
    def _render_case_conceptualization(self, document: Document, case: CaseConceptualizationModel):
        document.add_heading("Case conceptualization", level=1)

        # Relevant Life History
        document.add_heading("Relevant Life History", level=2)

        for index, item in enumerate(case.relevant_history_precipitants.relevant_life_history):
            document.add_paragraph(f'{index + 1}. {item}')

        # Precipitants
        document.add_heading("Precipitants", level=2)
        for index, item in enumerate(case.relevant_history_precipitants.precipitants):
            document.add_paragraph(f'{index + 1}. {item}')

        # Core belief
        for core_belief in case.core_intermediate_belief.core_beliefs:
            document.add_heading(f"Core belief type {core_belief.core_belief_type}", level=2)
            document.add_paragraph(
                f'Explanation: {core_belief.explanation}'
            )

            document.add_heading(f"Core belief type {core_belief.core_belief_type}", level=3)
            for index, client_core_belief in enumerate(core_belief.client_core_belief):
                document.add_paragraph(f'{index+1}. {client_core_belief}')


        # Intermediate Belief
        document.add_heading("Intermediate Belief", level=2)
        for index, belief in enumerate(case.core_intermediate_belief.intermediate_beliefs):
            document.add_paragraph(f'{index + 1}. {belief.intermediate_belief}')

        # Coping strategy
        document.add_heading("Coping strategy", level=2)
        for coping_strategy in case.coping_strategies:
            document.add_heading(coping_strategy.title, level=3)
            strategy_txt = f'''\
Summary: 
{coping_strategy.summary}

Rule: 
{coping_strategy.rule}

Attitude:
{coping_strategy.attitude}'''
            document.add_paragraph( strategy_txt)

        # Cognitive model
        document.add_heading("Cognitive model", level=2)
        for meaning_of_at, cognitive_data in zip(case.meaning_of_AT, case.cognitive_model):
            p = document.add_paragraph('')
            p.add_run('Situation: ').bold = True
            p.add_run(f'{cognitive_data.situation}\n').bold = False

            p.add_run('Automatic thought: ').bold = True
            p.add_run(f'{cognitive_data.automatic_thought}\n').bold = False

            p.add_run('Meaning of AT: ').bold = True
            p.add_run(f'{meaning_of_at.meaning_of_AT}\n').bold = False

            p.add_run('Emotion: ').bold = True
            p.add_run(f'{cognitive_data.emotion}\n').bold = False

            p.add_run('Behavior: ').bold = True
            p.add_run(f'{cognitive_data.behavior}\n\n').bold = False

        document.add_page_break()
# endregion

# Treatment Strategies
    def _render_treatment_strategies(self, document: Document, treatment_strategies: List[IssueTreatmentStrategy]):
        document.add_heading("Step by step treatment strategies", level=1)

        for index, treatment_strategy in enumerate(treatment_strategies):
            document.add_heading(f"Issue {index + 1}: {treatment_strategy.issue}", level=2)

            p = document.add_paragraph('')
            p.add_run('Goal: ').bold = True
            p.add_run(f'{treatment_strategy.goal}\n').bold = False

            p = document.add_paragraph('')
            p.add_run(f'Focus of stepped care: {treatment_strategy.focus_of_stepped_care}').bold = True

            document.add_paragraph(f'Number of steps: {len(treatment_strategy.treatment_steps) +1}')

            step_index = 0
            for step, criteria in zip(treatment_strategy.treatment_steps, treatment_strategy.treatment_evaluations):
                step_index += 1

                p = document.add_paragraph('')
                p.add_run('Phase-Specific Evaluation Criteria\n').bold = True
                p.add_run(f'{criteria.phase_specific_evaluation_criteria}').bold = False

                p = document.add_paragraph('')
                p.add_run(f'Step {step.title}').bold = True

                p = document.add_paragraph('')
                p.add_run(f'Therapeutic Goal: ').bold = True
                p.add_run(f'{step.therapeutic_goal}').bold = False

                p = document.add_paragraph('')
                p.add_run(f'Explanation of Technique: ').bold = True
                p.add_run(f'{step.explanation_of_technique}').bold = False

                p = document.add_paragraph('')
                p.add_run(f'Challenge: ').bold = True
                p.add_run(f'{criteria.challenge}').bold = False

                p = document.add_paragraph('')
                p.add_run(f'Recommended Step to Swift to: Step {criteria.recommended_swift_step_index+1}\n').bold = True
                p.add_run(f'{criteria.recommended_step_to_swift_to}').bold = False

        document.add_page_break()

    def _render_homeworks(self, document: Document, homework: HomeworkAssignment):
        document.add_heading("Homework", level=1)

        # Homework list
        for index, homework in enumerate(homework.homeworks):
            document.add_heading(f"Homework {index + 1}: {homework.title}", level=1)

            p = document.add_paragraph('')
            p.add_run(f'Goal: ').bold = True
            p.add_run(f'{homework.goal}').bold = False

            p = document.add_paragraph('')
            p.add_run(f'Task: ').bold = True
            p.add_run(f'{homework.task}').bold = False

            step_index = 0
            for step  in homework.steps:
                step_index += 1

                p = document.add_paragraph('')
                p.add_run(f'Step: {step_index}\n').bold = True
                p.add_run(f'{step.plan}').bold = False

                p = document.add_paragraph('')
                p.add_run(f'Example\n').bold = True
                p.add_run(f'{step.example}\n').bold = False


    def export(self, resp_model: SupervisorAnalysisRespModel):
        doc = Document()
        doc.add_heading("Report", level=0)

        self._render_case_conceptualization(doc, resp_model.case_conceptualization)
        self._render_treatment_strategies(doc, resp_model.issue_treatment_strategies)
        self._render_homeworks(doc, resp_model.homework_assignment)

        buffer = BytesIO()
        doc.save(buffer)  # write directly to memory
        buffer.seek(0)  # rewind so FastAPI reads from the start
        return buffer

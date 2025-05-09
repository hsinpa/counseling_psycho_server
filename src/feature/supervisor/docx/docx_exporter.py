from io import BytesIO
from docx import Document

from src.feature.supervisor.supervisor_model import SupervisorAnalysisRespModel, CaseConceptualizationModel


class SupervisorDocxExporter:

    def _render_case_conceptualization(self, document: Document, case: CaseConceptualizationModel):
        document.add_heading("Case conceptualization", level=1)
        document.add_heading("Relevant Life History", level=2)


    def export(self, resp_model: SupervisorAnalysisRespModel):
        doc = Document()
        doc.add_heading("Report", level=0)

        self._render_case_conceptualization(doc, resp_model.case_conceptualization)

        buffer = BytesIO()
        doc.save(buffer)  # write directly to memory
        buffer.seek(0)  # rewind so FastAPI reads from the start
        return buffer

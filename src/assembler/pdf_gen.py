from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from src.memory.schema import FullBook
import os

class PDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.output_dir = "output"
        os.makedirs(self.output_dir, exist_ok=True)

    def generate(self, book: FullBook) -> str:
        file_path = os.path.join(self.output_dir, f"{book.outline.title.replace(' ', '_')}.pdf")
        doc = SimpleDocTemplate(file_path, pagesize=letter)
        story = []

        # Styles
        title_style = ParagraphStyle(name='TitleStyle', parent=self.styles['Heading1'], alignment=TA_CENTER, fontSize=24, spaceAfter=20)
        heading_style = ParagraphStyle(name='HeadingStyle', parent=self.styles['Heading2'], fontSize=18, spaceAfter=12)
        body_style = ParagraphStyle(name='BodyStyle', parent=self.styles['BodyText'], alignment=TA_JUSTIFY, fontSize=12, spaceAfter=10)

        # Title Page
        story.append(Spacer(1, 100))
        story.append(Paragraph(book.outline.title, title_style))
        story.append(Spacer(1, 24))
        story.append(Paragraph(f"Written by AIuthor", heading_style))
        story.append(PageBreak())

        # Front Matter
        for key, content in book.front_matter.items():
            story.append(Paragraph(key.replace('_', ' ').title(), heading_style))
            story.append(Spacer(1, 12))
            story.append(Paragraph(content, body_style))
            story.append(PageBreak())

        # Body Chapters
        for chapter in book.chapters:
            story.append(Paragraph(f"Chapter {chapter.chapter_number}: {chapter.title}", heading_style))
            story.append(Spacer(1, 12))
            story.append(Paragraph(chapter.content, body_style))
            story.append(PageBreak())

        # Back Matter
        for key, content in book.back_matter.items():
            story.append(Paragraph(key.replace('_', ' ').title(), heading_style))
            story.append(Spacer(1, 12))
            story.append(Paragraph(content, body_style))
            story.append(PageBreak())

        doc.build(story)
        print(f"[PDFGenerator] PDF created: {file_path}")
        return file_path

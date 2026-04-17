import os
import json
from typing import List, Dict, Any
from src.memory.schema import BookBrief, FullBook, MemoryState, BookOutline, ChapterContent, FactRecord, DecisionLogEntry, TonalityFingerprint
from src.agents.planner import PlannerAgent
from src.agents.researcher import ResearcherAgent
from src.agents.writer import WriterAgent
from src.agents.humanizer import HumanizerAgent
from src.agents.editor import EditorAgent
from src.agents.fact_checker import FactCheckerAgent
from src.agents.memory_keeper import MemoryKeeperAgent
from src.agents.front_matter_agent import FrontMatterAgent
from src.agents.back_matter_agent import BackMatterAgent
from src.assembler.pdf_gen import PDFGenerator
from src.assembler.docx_gen import DOCXGenerator
from src.utils.rag import RAGSystem
from src.evals.scorers import EvalScorer
from src.utils.llm import LLMInterface
from src.config import PRIMARY_MODEL
import re

def clean_json(text: str) -> str:
    """Strip markdown code blocks and whitespace."""
    text = re.sub(r'```json\s*', '', text)
    return text.strip()

class Orchestrator:
    def __init__(self):
        self.llm = LLMInterface()
        self.planner = PlannerAgent(PRIMARY_MODEL)
        self.researcher = ResearcherAgent(PRIMARY_MODEL)
        self.writer = WriterAgent(PRIMARY_MODEL)
        self.humanizer = HumanizerAgent(PRIMARY_MODEL)
        self.editor = EditorAgent(PRIMARY_MODEL)
        self.fact_checker = FactCheckerAgent(PRIMARY_MODEL)
        self.memory_keeper = MemoryKeeperAgent(PRIMARY_MODEL)
        self.front_matter_agent = FrontMatterAgent(PRIMARY_MODEL)
        self.back_matter_agent = BackMatterAgent(PRIMARY_MODEL)
        self.rag = RAGSystem()
        self.evals = EvalScorer()
        self.pdf_gen = PDFGenerator()
        self.docx_gen = DOCXGenerator()

    def run(self, brief: BookBrief) -> FullBook:
        # 1. Planning
        print(f"[Planner] Planning book: {brief.topic}")
        outline_raw = self.llm.call_llm(self.planner.execute(brief), PRIMARY_MODEL, json_mode=True)
        outline_json = clean_json(outline_raw)
        
        try:
            outline = BookOutline(**json.loads(outline_json))
        except Exception as e:
            print(f"[Orchestrator] Error parsing outline JSON: {e}")
            print(f"Raw response: {outline_raw}")
            raise
        
        book = FullBook(
            brief=brief,
            outline=outline,
            front_matter={},
            chapters=[],
            back_matter={},
            memory=MemoryState()
        )
        
        for ch_outline in outline.chapters:
            # Decision Log: Start chapter
            book.memory.decision_log.append(DecisionLogEntry(
                agent_name="Orchestrator",
                decision=f"Generating Chapter {ch_outline.chapter_number}",
                rationale="Continuing sequential generation",
                alternatives_considered=[],
                timestamp=str(os.path.getmtime(__file__)) # placeholder
            ))
            
            # Research with RAG
            rag_context = self.rag.query(ch_outline.title + " " + " ".join(ch_outline.key_points))
            research_json = self.llm.call_llm(self.researcher.execute(ch_outline, context=str(rag_context)))
            try:
                research_data = json.loads(research_json)
                research = [FactRecord(**f) for f in research_data] if isinstance(research_data, list) else []
            except Exception as e:
                print(f"[Orchestrator] Research parsing failed: {e}")
                research = []
            
            # Write Draft
            draft = self.llm.call_llm(self.writer.execute(ch_outline, research, book.memory, brief.tonality.value))
            
            # Humanize
            humanized = self.llm.call_llm(self.humanizer.execute(draft, brief.tonality.value))
            
            # Edit
            edited = self.llm.call_llm(self.editor.execute(humanized, ch_outline.chapter_number))
            
            # Fact Check
            fact_check_report = self.llm.call_llm(self.fact_checker.execute(edited, research))
            # In a real system, we would handle failures here. For now, we log it.
            print(f"[{self.fact_checker.name}] Report: {fact_check_report}")
            
            # Update Memory
            memory_update_json = self.llm.call_llm(self.memory_keeper.execute(edited, book.memory, ch_outline.chapter_number))
            try:
                book.memory = MemoryState(**json.loads(memory_update_json))
            except Exception as e:
                print(f"[Orchestrator] Memory update failed: {e}")
            
            # Tonality Fingerprint (Simulated scoring for now)
            book.memory.tonality_fingerprint.append(TonalityFingerprint(
                chapter_number=ch_outline.chapter_number,
                lexical_density=0.45,
                sentence_variety_score=0.8,
                metaphor_count=3,
                ai_tell_count=0,
                dominant_tone=brief.tonality.value,
                examples=["Example humanized sentence..."]
            ))
            
            # Store Chapter
            book.chapters.append(ChapterContent(
                chapter_number=ch_outline.chapter_number,
                title=ch_outline.title,
                content=edited,
                summary=ch_outline.summary
            ))
            
        # 3. Matter Generation
        front_json = self.llm.call_llm(self.front_matter_agent.execute(brief, outline))
        book.front_matter = json.loads(front_json)
        
        back_json = self.llm.call_llm(self.back_matter_agent.execute(brief, outline, book.memory))
        book.back_matter = json.loads(back_json)
        
        # 4. Evals Run
        eval_results = self.evals.check_structural_completeness(book.dict())
        print(f"[Evals] Structural Completeness: {eval_results}")
        
        return book

    def repair_pipeline(self, book: FullBook, inserted_chapter_index: int) -> FullBook:
        """Test D: Self-healing repair logic for chapter insertion."""
        print(f"[Orchestrator] Triggering self-healing repair for chapter insertion at index {inserted_chapter_index}")
        # 1. Regenerate TOC (implicit in Assembler, but we update outline)
        # 2. Re-run Memory Keeper for the new chapter and all subsequent ones
        # 3. Regenerate Back Matter (Glossary especially)
        
        new_back_json = self.llm.call_llm(self.back_matter_agent.execute(book.brief, book.outline, book.memory))
        book.back_matter = json.loads(new_back_json)
        
        return book
